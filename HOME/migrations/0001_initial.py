# Generated by Django 4.2.5 on 2023-09-05 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('number', models.CharField(default=0, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.PositiveIntegerField(default=0)),
                ('brand', models.CharField(max_length=30)),
                ('proname', models.CharField(max_length=50)),
                ('starrating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('price', models.PositiveIntegerField()),
                ('feature', models.BooleanField(default=False)),
                ('newarrivals', models.BooleanField(default=False)),
                ('mainimg', models.ImageField(upload_to='DRESS')),
                ('subimg1', models.ImageField(upload_to='DRESS')),
                ('subimg2', models.ImageField(upload_to='DRESS')),
                ('subnimg3', models.ImageField(upload_to='DRESS')),
                ('subimg4', models.ImageField(upload_to='DRESS')),
            ],
        ),
        migrations.CreateModel(
            name='orderdescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.PositiveIntegerField(default=0)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('items', models.TextField(default='')),
                ('complete', models.BooleanField(default=False)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('address', models.TextField(default='')),
                ('payment_type', models.CharField(default='-', max_length=30)),
                ('cust', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HOME.customer')),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Customer Name')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('trans_id', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(default='PENDING', max_length=254, verbose_name='Payment Status')),
                ('provider_order_id', models.CharField(max_length=40, verbose_name='Order ID')),
                ('payment_id', models.CharField(max_length=36, verbose_name='Payment ID')),
                ('signature_id', models.CharField(max_length=128, verbose_name='Signature ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('cus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HOME.customer')),
            ],
        ),
        migrations.CreateModel(
            name='cartitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(default='', max_length=3)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('subtotal', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('orderid', models.CharField(max_length=10)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HOME.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HOME.product')),
            ],
        ),
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('d_s_a', models.TextField(default='')),
                ('landmark', models.CharField(default='', max_length=30)),
                ('pincode', models.PositiveIntegerField(default=0)),
                ('number', models.PositiveBigIntegerField(default=0)),
                ('cust', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HOME.customer')),
            ],
        ),
    ]