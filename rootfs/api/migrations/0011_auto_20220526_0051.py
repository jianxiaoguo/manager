# Generated by Django 3.2.11 on 2022-05-26 00:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20220524_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumerTaxInfo',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('no', models.CharField(blank=True, max_length=128, null=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'company'), (2, 'individual/sole trader'), (3, 'non-profit')])),
                ('name', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'not verified'), (1, 'verified')], db_index=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('no', models.CharField(blank=True, max_length=128, null=True)),
                ('rate', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('line1', models.CharField(max_length=128)),
                ('line2', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(blank=True, max_length=64, null=True)),
                ('state', models.CharField(blank=True, max_length=64, null=True)),
                ('country', models.CharField(max_length=64)),
                ('postcode', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='taxinfo',
            name='owner',
        ),
        migrations.DeleteModel(
            name='TaxRate',
        ),
        migrations.DeleteModel(
            name='TaxInfo',
        ),
    ]