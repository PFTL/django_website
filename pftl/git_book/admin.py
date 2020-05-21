from django.contrib import admin

from pftl.git_book.models import Subscription

admin.site.register((
    Subscription,
))