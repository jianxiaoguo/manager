# Generated by Django 3.2.11 on 2022-03-15 02:40

import api.utils
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('secret', models.CharField(auto_created=True, default=api.utils.generate_secret, max_length=64)),
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('url', models.URLField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PrepaidCard',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('amount', models.PositiveBigIntegerField()),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'normal'), (2, 'frozen')])),
                ('remark', models.TextField(null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'fault'), (2, 'security'), (3, 'service'), (4, 'product'), (5, 'promotion')])),
                ('body', models.TextField(db_index=True)),
                ('unread', models.BooleanField(default=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('app_id', models.CharField(db_index=True, max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=16)),
                ('unit', models.CharField(max_length=16)),
                ('usage', models.PositiveBigIntegerField(db_index=True)),
                ('timestamp', models.PositiveIntegerField(db_index=True)),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.cluster')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='FundFlow',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('direction', models.PositiveSmallIntegerField(choices=[(1, 'income'), (2, 'expense')])),
                ('fund_type', models.PositiveSmallIntegerField(choices=[(1, 'cash'), (2, 'order online payment')])),
                ('trading_id', models.CharField(max_length=128, null=True)),
                ('trading_type', models.PositiveSmallIntegerField(choices=[(1, 'account adjustment'), (2, 'recharge'), (4, 'refund'), (5, 'withdrawal'), (6, 'consumption')])),
                ('trading_channel', models.PositiveSmallIntegerField(choices=[(1, 'user blance'), (2, 'bank transfer'), (3, 'alipay'), (4, 'wechat'), (5, 'offline remittance'), (6, 'credit card')])),
                ('trading_channel_id', models.CharField(max_length=128, null=True)),
                ('associated_account_id', models.CharField(max_length=128, null=True)),
                ('period', models.PositiveIntegerField(db_index=True)),
                ('amount', models.PositiveBigIntegerField(db_index=True)),
                ('balance', models.PositiveBigIntegerField(db_index=True)),
                ('remark', models.TextField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ChargeUser',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('day', models.DateField()),
                ('owner_id', models.CharField(max_length=64)),
            ],
            options={
                'unique_together': {('day', 'owner_id')},
            },
        ),
        migrations.CreateModel(
            name='ChargeRule',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('type', models.CharField(db_index=True, max_length=32)),
                ('unit', models.CharField(db_index=True, max_length=32)),
                ('start', models.PositiveBigIntegerField(db_index=True)),
                ('end', models.PositiveBigIntegerField(db_index=True, null=True)),
                ('price', models.PositiveBigIntegerField()),
                ('group', models.PositiveBigIntegerField()),
                ('remark', models.TextField()),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.cluster')),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('start', 'end', 'type', 'unit')},
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('app_id', models.CharField(db_index=True, max_length=64)),
                ('type', models.CharField(max_length=16)),
                ('charge', models.JSONField(default=dict)),
                ('price', models.PositiveBigIntegerField()),
                ('period', models.PositiveIntegerField(db_index=True)),
                ('remark', models.TextField(null=True)),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.cluster')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'unique_together': {('app_id', 'type', 'period')},
            },
        ),
    ]
