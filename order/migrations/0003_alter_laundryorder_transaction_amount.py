# Generated by Django 4.2.3 on 2023-08-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_delivery_address_laundryorder_pickup_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundryorder',
            name='transaction_amount',
            field=models.FloatField(null=True),
        ),
    ]