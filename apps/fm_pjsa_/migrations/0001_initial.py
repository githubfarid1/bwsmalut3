# Generated by Django 4.2.3 on 2023-11-04 06:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=50, unique=True)),
                ('folder', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subfolder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('year', models.CharField(default='2023', max_length=4, validators=[django.core.validators.MinLengthValidator(4)])),
                ('folder', models.CharField(max_length=50, unique=True)),
                ('department', models.ForeignKey(db_column='department_id', default=None, on_delete=django.db.models.deletion.CASCADE, to='fm_pjsa.department')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('filename', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('subfolder', models.ForeignKey(db_column='subfolder_id', on_delete=django.db.models.deletion.CASCADE, to='fm_pjsa.subfolder')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
