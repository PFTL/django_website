# Generated by Django 3.1.6 on 2021-02-02 21:14

from django.db import migrations, models
import pftl.blog.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtailmarkdown.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blogpage_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='excerpt',
            field=models.TextField(blank=True, help_text='Short text to display in lists of posts', null=True),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='extended_body',
            field=wagtail.core.fields.StreamField([('content', wagtailmarkdown.blocks.MarkdownBlock(template='blog/markdown_block.html')), ('newsletter', pftl.blog.blocks.NewsletterSubscribe()), ('book', pftl.blog.blocks.BookInline()), ('video', wagtail.embeds.blocks.EmbedBlock())], null=True),
        ),
    ]