# Generated by Django 4.1.7 on 2023-04-17 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv_series', '0013_commentepisode'),
    ]

    operations = [
        migrations.AddField(
            model_name='serie',
            name='account',
            field=models.CharField(choices=[('Basic', 'Basic'), ('Premium', 'Premium')], default='Basic', max_length=30),
        ),
    ]