from django.db import models

from online_store.accounts.models import AppUser
from online_store.store.models import Product, Variation


class Order(models.Model):
    STATUS = (
        ('Нова', 'Нова'),
        ('Приета', 'Приета'),
        ('Завършена', 'Завършена'),
        ('Отказана', 'Отказана'),
    )

    user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=20, )
    first_name = models.CharField(max_length=50, )
    last_name = models.CharField(max_length=50, )
    phone = models.CharField(max_length=13, )
    address = models.CharField(max_length=50, )
    city = models.CharField(max_length=50, )
    order_note = models.CharField(max_length=100, blank=True, )
    order_total = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='Нова')
    ip = models.CharField(blank=True, max_length=20, )
    is_ordered = models.BooleanField(default=False, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name


from .signals import *
