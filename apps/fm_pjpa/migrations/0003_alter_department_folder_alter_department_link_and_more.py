# Generated by Django 4.2.3 on 2023-11-06 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fm_pjpa', '0002_department_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='folder',
            field=models.CharField(max_length=125, unique=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='link',
            field=models.CharField(max_length=125, unique=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='slug',
            field=models.SlugField(default=None, max_length=125, unique=True),
        ),
    ]