# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_courseclass_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 26, 363548, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendance',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 32, 534152, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 49, 80993, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 51, 295769, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseclass',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 54, 530304, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseclass',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 55, 862349, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='department',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 57, 193648, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='department',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 58, 667422, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='designation',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 35, 59, 976202, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='designation',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 1, 285712, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faculty',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 2, 690112, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faculty',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 3, 989712, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='markingunit',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 5, 408581, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='markingunit',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 6, 653564, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 7, 885601, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 9, 269558, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 10, 521135, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 11, 895423, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semester',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 13, 150995, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='semester',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 14, 616965, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 16, 575400, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 17, 957805, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='time',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 19, 626699, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='time',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 11, 13, 36, 20, 981539, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
