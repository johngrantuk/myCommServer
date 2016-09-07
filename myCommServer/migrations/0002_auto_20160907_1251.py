# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myCommServer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermsg',
            old_name='users',
            new_name='user',
        ),
        migrations.AddField(
            model_name='usermsg',
            name='destinationId',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
