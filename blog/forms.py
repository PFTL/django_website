from django.contrib.syndication.views import Feed

from blog.models import BlogPage


class BlogsFeed(Feed):
    title = "Python for the lab"
    link = "/blog"
    description = "Learn how to use Python for controlling your experiments"

    def items(self):
        return BlogPage.objects.live().order_by('-date_published')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.introduction