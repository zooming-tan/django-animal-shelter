# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers
import django.db.models.deletion
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('breed', models.CharField(max_length=50, choices=[('Border Collie', 'Border Collie'), ('Bull Terrier', 'Bull Terrier'), ('Mastiff', 'Mastiff')], blank=True, null=True)),
                ('age', models.CharField(max_length=25, choices=[('Puppy', 'Puppy'), ('Young', 'Young'), ('Adult', 'Adult'), ('Senior', 'Senior')], blank=True, null=True)),
                ('sex', models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)),
                ('size', models.CharField(max_length=20, choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], blank=True, null=True)),
                ('is_neutered', models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('biography', models.TextField(max_length=1500, help_text='A short introduction', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('img', models.ImageField(null=True, blank=True, upload_to='photo/')),
                ('animal', models.ForeignKey(to='animal.Animal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='animal',
            name='cover',
            field=models.OneToOneField(to='animal.Photo', related_name='+', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True),
        ),
        migrations.AddField(
            model_name='animal',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', verbose_name='Tags', blank=True, through='taggit.TaggedItem', help_text='A comma-separated list of tags.'),
        ),
    ]
