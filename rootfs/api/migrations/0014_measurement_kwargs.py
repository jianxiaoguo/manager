# Generated by Django 4.2.10 on 2024-03-25 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_measurement_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='kwargs',
            field=models.JSONField(default=dict),
        ),
    ]
