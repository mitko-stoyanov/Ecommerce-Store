# Generated by Django 4.1.4 on 2023-01-07 15:22

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_alter_discount_discount_percent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=200)),
                ('postal_code', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('notes', models.TextField(max_length=350)),
            ],
        ),
    ]