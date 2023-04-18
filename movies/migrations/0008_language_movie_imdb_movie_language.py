# Generated by Django 4.1.7 on 2023-03-31 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_genre_created_at_genre_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Dil',
                'verbose_name_plural': 'Dillər',
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb',
            field=models.FloatField(default=8.7),
        ),
        migrations.AddField(
            model_name='movie',
            name='language',
            field=models.ManyToManyField(default='turkce', to='movies.language'),
        ),
    ]
