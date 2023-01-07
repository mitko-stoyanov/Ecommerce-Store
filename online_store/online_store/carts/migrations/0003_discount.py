# Generated by Django 4.1.4 on 2023-01-06 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('owner', models.CharField(max_length=50)),
                ('discount_percent', models.IntegerField()),
                ('times_used', models.IntegerField(default=0)),
            ],
        ),
    ]