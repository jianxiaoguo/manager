# Generated by Django 2.2.18 on 2021-05-26 02:34

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20210526_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='charge_rule_info',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
        migrations.AlterField(
            model_name='bill',
            name='resource_info',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
    ]
