# Generated by Django 4.1.7 on 2023-03-30 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_actor_options_alter_genre_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2023-03-30 14:05:30.123456+03:00'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genre',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
