# Generated by Django 4.2.3 on 2023-08-06 14:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.UUID('153096d4-9d18-47fe-8ca3-07334d4b0677'), primary_key=True, serialize=False)),
                ('laundry_order_id', models.UUIDField()),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(null=True)),
            ],
        ),
    ]
