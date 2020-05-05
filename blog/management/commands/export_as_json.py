import json
import os

from django.core.management import BaseCommand

from blog.models import BlogPage


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '/webapps/pftl/articles_archive'
        blog_posts = BlogPage.objects.all()
        for post in blog_posts:
            data = {
                'title': post.title,
                'subtitle': post.subtitle,
                'image_data': post.image_data,
                'tags': [tag.slug for tag in post.get_tags],
                'date_published': f'{post.date_published:}',
                'body': post.body,
            }
            with open(os.path.join(file_path, post.title+'.json'), 'w') as f:
                json.dump(data, f)
