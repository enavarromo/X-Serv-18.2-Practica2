# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acorta', '0002_auto_20160407_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='urlCortas',
            fields=[
                ('urlCorta', models.TextField(serialize=False, primary_key=True)),
                ('urlLarga', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='urlLargas',
            fields=[
                ('urlLarga', models.TextField(serialize=False, primary_key=True)),
                ('urlCorta', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Pages',
        ),
    ]
