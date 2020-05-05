import json
import os

from django.core.management import BaseCommand

from pftl.blog.models import BlogPage, BlogIndexPage


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '/webapps/pftl/articles_archive'
        index_page = BlogIndexPage.objects.get_or_create(title='Blog')[0].specific
        for file in os.listdir(file_path):
            with open(os.path.join(file_path, file), 'r') as f:
                data = json.load(f)
                page = BlogPage(**data)
                index_page.add_child(page)
