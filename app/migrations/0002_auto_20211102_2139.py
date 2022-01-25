# Generated by Django 3.2.8 on 2021-11-02 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bio',
            name='image',
        ),
        migrations.AddField(
            model_name='bio',
            name='skill_t',
            field=models.CharField(default='skill', max_length=1024),
        ),
        migrations.AddField(
            model_name='bio',
            name='skill_w',
            field=models.CharField(default='skill', max_length=1024),
        ),
        migrations.AlterField(
            model_name='bio',
            name='intro_text',
            field=models.CharField(default='intro', max_length=1024),
        ),
        migrations.AlterField(
            model_name='bio',
            name='outro_text',
            field=models.CharField(blank=True, default='outro', max_length=1024, null=True),
        ),
    ]
