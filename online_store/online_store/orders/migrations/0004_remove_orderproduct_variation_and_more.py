# Generated by Django 4.1.4 on 2023-01-11 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_variation'),
        ('orders', '0003_orderproduct_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
