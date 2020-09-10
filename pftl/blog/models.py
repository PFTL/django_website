from bs4 import BeautifulSoup
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.shortcuts import redirect, render
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase, Tag
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailmarkdown.blocks import MarkdownBlock
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField
from wagtailmarkdown.utils import render_markdown

from pftl.blog.blocks import NewsletterSubscribe, BookInline


class BlogPeopleRelationship(Orderable, models.Model):
    """ This allows to add several people to the same Page, in case there are multiple authors associated with an
    article.
    """
    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        'base.People', related_name='person_blog_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('people')
    ]


class BlogPageTag(TaggedItemBase):
    """ Tagging System for articles
    """
    content_object = ParentalKey('BlogPage', related_name='tagged_items', on_delete=models.CASCADE)


class BlogPage(Page):
    """ This is the core of the Blog app. BlogPage are individual articles
    """
    subtitle = models.CharField(blank=True, max_length=255)

    body = MarkdownField(blank=True)

    extended_body = StreamField([
        ('content', MarkdownBlock(template='blog/markdown_block.html')),
        ('newsletter', NewsletterSubscribe()),
        ('book', BookInline()),
    ],
        null=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Header Image, used also for social sharing'
    )

    image_data = RichTextField(
        blank=True,
        null=True,
        help_text='Information about the header image, to appear after the article')

    video = models.TextField(
        blank=True,
        null=True,
        help_text='If the article has an associated video, it will appear as the header'
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date_published = models.DateField(
        "Date article published", blank=True, null=True
    )

    allow_comments = models.BooleanField(default=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel('extended_body'),
        MarkdownPanel('body'),
        ImageChooserPanel('image'),
        FieldPanel('image_data'),
        FieldPanel('video'),
        FieldPanel('date_published'),
        InlinePanel(
            'blog_person_relationship', label="Author(s)",
            panels=None, min_num=1),
        FieldPanel('tags'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('allow_comments'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    def authors(self):
        """
        Returns the BlogPage's related People. Again note that we are using
        the ParentalKey's related_name from the BlogPeopleRelationship model
        to access these objects. This allows us to access the People objects
        with a loop on the template. If we tried to access the blog_person_
        relationship directly we'd print `blog.BlogPeopleRelationship.None`
        """
        authors = [
            n.people for n in self.blog_person_relationship.all()
        ]

        return authors

    @property
    def first_author(self):
        return self.authors()[-1]

    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ['BlogIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []

    def get_absolute_url(self):
        return self.specific.url

    def get_context(self, request):
        context = super(BlogPage, self).get_context(request)
        context['latest_articles'] = BlogPage.objects.live().order_by('-date_published')[:5]
        context['intro_class'] = 'blog article'
        return context

    @property
    def introduction(self):
        html = render_markdown(self.body)
        soup = BeautifulSoup(html, "html.parser")
        try:
            introduction = soup.find('p').text
            return introduction
        except AttributeError:
            return None

    class Meta:
        ordering = ['-date_published']


class BlogIndexPage(RoutablePageMixin, Page):
    """ Index page for the Blog.
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    # Speficies that only BlogPage objects can live under this index page
    subpage_types = ['BlogPage']

    # Defines a method to access the children of the page (e.g. BlogPage
    # objects). On the demo site we use this on the HomePage
    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)

        all_posts = BlogPage.objects.descendant_of(
            self).live().order_by(
            '-date_published')
        paginator = Paginator(all_posts, 20)
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        context["intro_class"] = "blog"
        return context

    # This defines a Custom view that utilizes Tags. This view will return all
    # related BlogPages for a given Tag or redirect back to the BlogIndexPage.
    # More information on RoutablePages is at
    # http://docs.wagtail.io/en/latest/reference/contrib/routablepage.html
    @route(r'^tags/$', name='tag_archive')
    @route(r'^tags/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):
        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no blog posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'blog/blog_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = BlogPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # Returns the list of Tags for all child posts of this BlogPage.
    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            # Not tags.append() because we don't want a list of lists
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags
