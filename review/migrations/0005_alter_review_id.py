# Generated by Django 4.2.3 on 2023-08-07 13:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_alter_review_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.UUIDField(auto_created=True, default=uuid.UUID('d6f86764-9ed1-4d74-82e8-822ff3002371'), primary_key=True, serialize=False),
        ),
    ]