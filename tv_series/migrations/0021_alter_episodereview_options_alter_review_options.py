# Generated by Django 4.1.7 on 2023-08-22 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tv_series', '0020_alter_episodereview_options_alter_review_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='episodereview',
            options={'verbose_name': 'Epizod Reyting', 'verbose_name_plural': 'Epizod Reyting'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Serial Reyting', 'verbose_name_plural': 'Serial Reyting'},
        ),
    ]
