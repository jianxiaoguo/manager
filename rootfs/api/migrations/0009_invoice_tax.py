# Generated by Django 3.2.11 on 2022-05-23 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_invoice_prepaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='tax',
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
