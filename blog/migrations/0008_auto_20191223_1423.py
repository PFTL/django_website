# Generated by Django 2.2.9 on 2019-12-23 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20191223_1047'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpage',
            options={'ordering': ['-date_published']},
        ),
    ]
