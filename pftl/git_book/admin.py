from django.contrib import admin

from git_book.models import Subscription

admin.site.register((
    Subscription,
))