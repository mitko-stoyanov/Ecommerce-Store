from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from online_store.store.models import Product

from phonenumber_field.modelfields import PhoneNumberField


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


class Discount(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True
    )

    owner = models.CharField(
        max_length=50,
    )

    discount_percent = models.IntegerField(
        validators=(
            MaxValueValidator(100),
            MinValueValidator(1),
        ),
    )

    times_used = models.IntegerField(
        default=0,
    )
