# Generated by Django 4.1.7 on 2023-04-15 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0018_alter_movie_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='watched_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
