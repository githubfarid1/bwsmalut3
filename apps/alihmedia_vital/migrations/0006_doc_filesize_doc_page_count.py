# Generated by Django 4.2.3 on 2023-08-29 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alihmedia_vital', '0005_doc_doc_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='filesize',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='doc',
            name='page_count',
            field=models.SmallIntegerField(null=True),
        ),
    ]
