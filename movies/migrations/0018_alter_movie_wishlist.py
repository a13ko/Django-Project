# Generated by Django 4.1.7 on 2023-04-08 18:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0017_movie_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='wishlist',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]