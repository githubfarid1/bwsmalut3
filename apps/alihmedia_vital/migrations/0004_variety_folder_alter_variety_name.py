# Generated by Django 4.2.3 on 2023-08-29 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alihmedia_vital', '0003_remove_doc_orinot_alter_doc_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='variety',
            name='folder',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='variety',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]