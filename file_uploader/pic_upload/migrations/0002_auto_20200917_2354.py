# Generated by Django 3.1 on 2020-09-17 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pic_upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='picture',
            options={'ordering': ['-date']},
        ),
        migrations.RemoveField(
            model_name='picture',
            name='image',
        ),
        migrations.AddField(
            model_name='picture',
            name='image_url',
            field=models.TextField(default='ok'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picture',
            name='title',
            field=models.CharField(blank=True, default='Unknown', max_length=100),
        ),
    ]
