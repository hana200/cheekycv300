# Generated by Django 3.2.8 on 2022-07-25 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_web_wl5'),
    ]

    operations = [
        migrations.AddField(
            model_name='web',
            name='wl5',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
