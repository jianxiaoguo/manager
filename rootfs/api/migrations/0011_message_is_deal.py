# Generated by Django 2.2.18 on 2021-03-30 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210324_0549'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_deal',
            field=models.BooleanField(default=False),
        ),
    ]