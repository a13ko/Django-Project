# Generated by Django 4.1.7 on 2023-03-21 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='username',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
