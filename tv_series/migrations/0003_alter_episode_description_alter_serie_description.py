# Generated by Django 4.1.7 on 2023-03-29 19:40

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tv_series', '0002_alter_episode_description_alter_serie_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='serie',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
