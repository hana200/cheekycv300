# Generated by Django 3.2.8 on 2021-11-16 15:08

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20211116_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pimg',
            name='url',
        ),
        migrations.AlterField(
            model_name='pimg',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=app.models.path_and_rename_overwrite),
        ),
    ]
