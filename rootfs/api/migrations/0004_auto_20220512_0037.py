# Generated by Django 3.2.11 on 2022-05-12 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_invoiceaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Unsettled'), (1, 'Unpaid'), (2, 'Paid'), (3, 'No Charge')], db_index=True),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='address1',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='address2',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='city',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='country',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='other',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='postcode',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceaddress',
            name='state',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.CreateModel(
            name='PaymentCard',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=16)),
                ('brand', models.CharField(max_length=16)),
                ('last4', models.CharField(max_length=4)),
                ('line1', models.CharField(max_length=128)),
                ('line2', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('postcode', models.CharField(blank=True, max_length=64, null=True)),
                ('exp_year', models.PositiveSmallIntegerField(db_index=True)),
                ('exp_month', models.PositiveSmallIntegerField(db_index=True)),
                ('extra_data', models.JSONField(blank=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
