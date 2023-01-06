from django.contrib.auth import get_user_model
from django.db import models

from online_store.store.models import Product


class Cart(models.Model):
    User = get_user_model()

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'Owner: {self.owner.name}'


class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
    )

    quantity = models.IntegerField()

    is_active = models.BooleanField(
        default=True,
    )

    def sub_total(self):
        return self.product.price * self.quantity

