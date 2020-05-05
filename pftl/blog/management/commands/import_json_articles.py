import json
import os

from django.core.management import BaseCommand

from pftl.blog.models import BlogPage


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = '/webapps/pftl/articles_archive'
        for file in os.listdir(file_path):
            with open(file, 'r') as f:
                data = json.load(f)
                page = BlogPage(**data)
                page.save()