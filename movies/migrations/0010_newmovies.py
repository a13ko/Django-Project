# Generated by Django 4.1.7 on 2023-04-05 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_alter_movie_imdb_alter_movie_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewMovies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('release_date', models.DateField()),
                ('poster', models.ImageField(upload_to='posters/')),
                ('genres', models.ManyToManyField(to='movies.genre')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
