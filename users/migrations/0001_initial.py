# Generated by Django 4.1 on 2022-09-23 12:26

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('role', models.CharField(choices=[('B', 'Buyer'), ('S', 'Seller')], default='B', max_length=1, verbose_name='Role')),
                ('phone_number', models.CharField(max_length=255, verbose_name='Phone number')),
                ('date_of_birth', models.DateTimeField(null=True, verbose_name='Your birthday')),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=60)),
                ('address', models.CharField(max_length=60)),
                ('postal_code', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='BuyerProfile',
            fields=[
                ('buyer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('delivery_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.address')),
            ],
        ),
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(default='', max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.buyerprofile')),
                ('product_codes', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveBigIntegerField(), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='OnSale',
            fields=[
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.sellerprofile')),
                ('product_codes', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveBigIntegerField(), default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('buyer_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.buyerprofile')),
                ('product_codes', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveBigIntegerField(), default=list, size=None)),
                ('size', models.CharField(default='', max_length=10)),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]