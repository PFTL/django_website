from django.contrib.syndication.views import Feed

from pftl.blog.models import BlogPage


class BlogsFeed(Feed):
    title = "Python for the lab blog articles"
    link = "/feed/"
    description = "All the articles as they are published"

    def items(self):
        return BlogPage.objects.live().order_by('-date_published')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.introduction