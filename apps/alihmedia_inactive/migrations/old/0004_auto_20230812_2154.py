# Generated by Django 4.2.3 on 2023-08-12 21:54

from django.db import migrations
from uuid import uuid4

class Migration(migrations.Migration):
    def populate_uuid(apps, schema_editor):
        Doc = apps.get_model('alihmedia_inactive', 'Doc')
        docs = list(Doc.objects.all())
        for doc in docs:
            doc.uuid_id = uuid4()
        Doc.objects.bulk_update(docs, ['uuid_id'])    

    dependencies = [
        ('alihmedia_inactive', '0005_doc_uuid_id'),
    ]

    operations = [
            migrations.RunPython(populate_uuid)
        ]