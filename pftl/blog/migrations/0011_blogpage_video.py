# Generated by Django 3.0.5 on 2020-09-10 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200730_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='video',
            field=models.TextField(blank=True, help_text='If the article has an associated video, it will appear as the header', null=True),
        ),
    ]