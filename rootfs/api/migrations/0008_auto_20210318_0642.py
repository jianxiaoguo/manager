# Generated by Django 2.2.14 on 2021-03-18 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210318_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargerule',
            name='price_unit',
            field=models.CharField(max_length=64),
        ),
    ]
