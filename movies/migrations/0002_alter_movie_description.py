# Generated by Django 4.1.7 on 2023-03-29 19:34

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=djrichtextfield.models.RichTextField(),
        ),
    ]