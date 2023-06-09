# Generated by Django 4.1.7 on 2023-04-06 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_movie_age_limit_movie_running_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='age_limit',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='running_time',
            field=models.PositiveIntegerField(),
        ),
    ]
