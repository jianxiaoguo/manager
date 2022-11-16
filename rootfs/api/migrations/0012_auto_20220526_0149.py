# Generated by Django 3.2.11 on 2022-05-26 01:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20220526_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderTaxInfo',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('no', models.CharField(blank=True, db_index=True, max_length=128, null=True)),
                ('rate', models.PositiveSmallIntegerField()),
                ('city', models.CharField(blank=True, max_length=64, null=True)),
                ('state', models.CharField(blank=True, max_length=64, null=True)),
                ('country', models.CharField(max_length=64)),
            ],
            options={
                'unique_together': {('country', 'state', 'city')},
            },
        ),
        migrations.DeleteModel(
            name='ServiceProvider',
        ),
    ]