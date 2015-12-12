# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('animal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='img',
            field=sorl.thumbnail.fields.ImageField(upload_to='photo/', null=True, blank=True),
        ),
    ]
