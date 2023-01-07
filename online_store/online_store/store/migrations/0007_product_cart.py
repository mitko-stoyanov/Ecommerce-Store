# Generated by Django 4.1.4 on 2023-01-05 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
        ('store', '0006_remove_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='carts.cart'),
            preserve_default=False,
        ),
    ]