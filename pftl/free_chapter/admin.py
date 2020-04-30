from django.contrib import admin

from pftl.free_chapter.models import People, FreeChapter

admin.site.register((
    People,
    FreeChapter))