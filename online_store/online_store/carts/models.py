from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from online_store.store.models import Product, Variation


class Cart(models.Model):
    User = get_user_model()

    date_added = models.DateTimeField(auto_now_add=True,)

    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)

    def __str__(self):
        return f'Owner: {self.owner.name}'


class CartItem(models.Model):
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True, )

    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    variations = models.ManyToManyField(Variation, blank=True,)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product


class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True,)
    owner = models.CharField(max_length=50,)
    discount_percent = models.IntegerField(
        validators=(
            MaxValueValidator(100),
            MinValueValidator(1),
        ),
    )
    times_used = models.IntegerField(default=0,)
