# Generated by Django 2.2.14 on 2021-03-18 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210318_0532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funding',
            name='app_id',
        ),
        migrations.RemoveField(
            model_name='funding',
            name='cluster',
        ),
    ]
