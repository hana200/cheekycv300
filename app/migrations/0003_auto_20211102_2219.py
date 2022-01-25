# Generated by Django 3.2.8 on 2021-11-02 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211102_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bio',
            name='intro_text',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='bio',
            name='outro_text',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='bio',
            name='skill_t',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='bio',
            name='skill_w',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='cv',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='JOB_cv', to='app.cv'),
        ),
    ]
