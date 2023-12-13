# Generated by Django 4.1 on 2023-04-01 03:19

import checkouts.models
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
        ('products', '0003_alter_category_media_alter_product_media_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('note', models.TextField(blank=True, default='')),
                ('currency', models.CharField(max_length=3)),
                ('country', django_countries.fields.CountryField(default=checkouts.models.get_default_country, max_length=2)),
                ('total_net_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('total_gross_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('subtotal_net_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('subtotal_gross_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('shipping_price_net_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('shipping_price_gross_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('shipping_tax_rate', models.DecimalField(decimal_places=4, default=Decimal('0.0'), max_digits=5)),
                ('price_expiration', models.DateTimeField(default=django.utils.timezone.now)),
                ('discount_amount', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=12)),
                ('discount_name', models.CharField(blank=True, max_length=255, null=True)),
                ('translated_discount_name', models.CharField(blank=True, max_length=255, null=True)),
                ('voucher_code', models.CharField(blank=True, max_length=255, null=True)),
                ('redirect_url', models.URLField(blank=True, null=True)),
                ('tracking_code', models.CharField(blank=True, max_length=255, null=True)),
                ('language_code', models.CharField(choices=[('en', 'English'), ('ar', 'العربيّة')], default='en', max_length=35)),
                ('tax_exemption', models.BooleanField(default=False)),
                ('billing_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='accounts.address')),
                ('shipping_address', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='accounts.address')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='checkouts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-last_change', 'pk'),
            },
        ),
        migrations.CreateModel(
            name='CheckoutMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='metadata_storage', to='checkouts.checkout')),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutLine',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('old_id', models.PositiveIntegerField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('price_override', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('currency', models.CharField(max_length=3)),
                ('total_price_net_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('total_price_gross_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=12)),
                ('tax_rate', models.DecimalField(decimal_places=4, default=Decimal('0.0'), max_digits=5)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='checkouts.checkout')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='products.productvariant')),
            ],
            options={
                'ordering': ('created_at', 'id'),
            },
        ),
    ]
