from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel, StreamFieldPanel, PageChooserPanel, \
    InlinePanel, RichTextFieldPanel
from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from base.blocks import BaseStreamBlock


@register_snippet
class People(index.Indexed, ClusterableModel):
    """ Model to store information about who participated in the development of articles, tutorials, etc.
    """
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    subtitle = models.CharField("Short information", max_length=254)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname="col6"),
                FieldPanel('last_name', classname="col6"),
            ])
        ], "Name"),
        FieldPanel('subtitle'),
        ImageChooserPanel('image')
    ]

    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition('fill-50x50').img_tag()
        except:  # noqa: E722 FIXME: remove bare 'except:'
            return ''

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


class BasePage(Page):
    """ Basic page that takes an introduction, an image, and a body. This can be used to write the about us page, etc.
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    content_panels = Page.content_panels + [
        RichTextFieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
    ]

    def get_context(self, request):
        context = super(BasePage, self).get_context(request)
        # Very silly way of getting the first word of the title and use it as template context
        c = self.title.split(' ')[0].lower()
        context['wrapper_class'] = c
        context['intro_class'] = c
        return context


class BooksPage(BasePage):
    def get_context(self, request):
        context = super(BasePage, self).get_context(request)
        context['intro_class'] = 'about book'
        context['wrapper_class'] = ''
        print(context)
        return context


class HomePage(Page):
    """ Home Page, needs to respect the sections available in the template.
    """

    # This is the text that goes next to the image
    hero_text = RichTextField(
        help_text='Write an introduction for the Landing Page'
    )

    featured_section = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='This is what will be shown below the navbar (e.g. latest articles)',
        verbose_name='Featured Section'
    )

    content_panels = Page.content_panels + [
            FieldPanel('hero_text'),
            PageChooserPanel('featured_section'),
        ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['wrapper_class'] = 'home'
        context['intro_class'] = 'home'
        return context

    def __str__(self):
        return self.title

class FormField(AbstractFormField):
    """ Quick and dirty solution to add forms through the Wagtail admin
    """
    page = ParentalKey('FormPage', related_name='form_fields', on_delete=models.CASCADE)


class FormPage(AbstractEmailForm):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BaseStreamBlock())
    thank_you_text = RichTextField(blank=True)

    # Note how we include the FormField object via an InlinePanel using the
    # related_name value
    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
