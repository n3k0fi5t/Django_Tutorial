# Generated by Django 3.1 on 2020-09-01 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200901_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurantreview',
            old_name='restauant',
            new_name='restaurant',
        ),
    ]
