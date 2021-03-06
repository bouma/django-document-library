# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.file
import filer.fields.folder
from django.conf import settings
import filer.fields.image
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('cms', '0011_auto_20150419_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField(null=True, verbose_name='Position', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('position', models.PositiveIntegerField(null=True, verbose_name='Position', blank=True)),
                ('is_on_front_page', models.BooleanField(default=False, verbose_name='Is on front page')),
                ('source_url', models.URLField(help_text='Use this if you want to give credit for a downloadable file.', verbose_name='Source URL', blank=True)),
                ('download_url', models.URLField(help_text='Use this if you want to link to a file instead of self-hosting it', verbose_name='Download URL', blank=True)),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('document_date', models.DateTimeField(null=True, verbose_name='Document date', blank=True)),
            ],
            options={
                'ordering': ('position', '-document_date'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('slug', models.SlugField(max_length=32, verbose_name='Slug')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentCategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='document_library.DocumentCategory', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'document_library_documentcategory_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('document', models.ForeignKey(verbose_name='Document', to='document_library.Document')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='DocumentTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Short description', blank=True)),
                ('copyright_notice', models.CharField(max_length=1024, verbose_name='Copyright notice', blank=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
                ('meta_description', models.TextField(max_length=512, verbose_name='Meta description', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('filer_file', filer.fields.file.FilerFileField(related_name='document_files', verbose_name='File', blank=True, to='filer.File', null=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='document_library.Document', null=True)),
                ('thumbnail', filer.fields.file.FilerFileField(related_name='document_thumbnails', verbose_name='Thumbnail', blank=True, to='filer.File', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'document_library_document_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='documenttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentcategorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='document',
            name='category',
            field=models.ForeignKey(verbose_name='Category', blank=True, to='document_library.DocumentCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='content',
            field=cms.models.fields.PlaceholderField(related_name='documents', slotname='document_library_content', editable=False, to='cms.Placeholder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='folder',
            field=filer.fields.folder.FilerFolderField(related_name='document_folders', verbose_name='Folder', blank=True, to='filer.Folder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='image',
            field=filer.fields.image.FilerImageField(related_name='document_images', verbose_name='Image', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='document',
            field=models.ForeignKey(verbose_name='Document', to='document_library.Document'),
            preserve_default=True,
        ),
    ]
