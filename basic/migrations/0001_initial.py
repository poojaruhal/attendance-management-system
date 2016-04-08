# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CourseClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('acronym', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('acronym', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('faculty_id', models.CharField(max_length=100)),
                ('department', models.ForeignKey(to='basic.Department')),
                ('designation', models.ForeignKey(to='basic.Designation')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MarkingUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('query', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student_id', models.CharField(max_length=100)),
                ('mobile_number', models.CharField(max_length=10)),
                ('parents_mobile_number', models.CharField(max_length=10)),
                ('parents_email', models.CharField(max_length=100)),
                ('department', models.ForeignKey(to='basic.Department')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=10)),
                ('hour', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='markingunit',
            name='room',
            field=models.ForeignKey(to='basic.Room', blank=True),
        ),
        migrations.AddField(
            model_name='courseclass',
            name='faculty',
            field=models.ForeignKey(to='basic.Faculty'),
        ),
        migrations.AddField(
            model_name='courseclass',
            name='room',
            field=models.ForeignKey(to='basic.Room'),
        ),
        migrations.AddField(
            model_name='courseclass',
            name='semester',
            field=models.ForeignKey(to='basic.Semester'),
        ),
        migrations.AddField(
            model_name='courseclass',
            name='time',
            field=models.ForeignKey(to='basic.Time'),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(to='basic.Department'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='course_class',
            field=models.ForeignKey(to='basic.CourseClass'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(to='basic.Student'),
        ),
    ]
