from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class CoursePage(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Header Image, used also for social sharing'
    )

    body = RichTextField(blank=False, help_text='This will appear as the core information on the page')

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
        ImageChooserPanel('image'),
    ]

    def get_context(self, request, **kwargs):
        context = super(CoursePage, self).get_context(request, **kwargs)
        courses = CoursePage.objects.live()
        context['courses'] = courses
        context['intro_class'] = 'blog article'
        return context
