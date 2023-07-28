# Generated by Django 4.2.3 on 2023-07-22 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MarketApp', '0004_coupon'),
        ('Accounts', '0002_cart_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MarketApp.coupon'),
        ),
    ]