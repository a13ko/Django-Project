# Generated by Django 4.1.7 on 2023-03-29 19:00

from django.db import migrations, models
import django.db.models.deletion
import services.uploader


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('code', models.SlugField(editable=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('episode_number', models.IntegerField()),
                ('release_date', models.DateField()),
                ('description', models.TextField()),
                ('duration', models.DurationField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('code', models.SlugField(editable=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('director', models.CharField(max_length=255)),
                ('release_date', models.DateField()),
                ('description', models.TextField()),
                ('poster', models.ImageField(upload_to='posters/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SerieGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=services.uploader.Uploader.upload_image_serie)),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tv_series.serie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField()),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tv_series.serie')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EpisodeGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('video', models.FileField(upload_to=services.uploader.Uploader.upload_video_episode)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tv_series.episode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tv_series.season'),
        ),
    ]
