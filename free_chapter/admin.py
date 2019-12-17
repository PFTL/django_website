from django.contrib import admin

from free_chapter.models import People, FreeChapter

admin.site.register((
    People,
    FreeChapter))