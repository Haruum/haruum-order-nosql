# Generated by Django 4.2.3 on 2023-08-08 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_laundryorder_transaction_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='laundryorder',
            name='has_review',
            field=models.BooleanField(default=False),
        ),
    ]