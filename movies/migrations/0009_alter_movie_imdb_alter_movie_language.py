# Generated by Django 4.1.7 on 2023-03-31 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_language_movie_imdb_movie_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='movie',
            name='language',
            field=models.ManyToManyField(to='movies.language'),
        ),
    ]