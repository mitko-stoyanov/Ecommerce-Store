from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from online_store.accounts.models import AppUser


class Category(models.Model):
    category_name = models.CharField(
        max_length=50,
        unique=True,
    )

    # Slug is a newspaper term. A slug is a short label for something, containing only letters, numbers,
    # underscores or hyphens. They’re generally used in URLs.

    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    image = models.ImageField(
        upload_to='photos/categories',
    )

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])


class Product(models.Model):
    product_name = models.CharField(
        max_length=200,
        unique=True,
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
    )

    description = models.TextField(
        max_length=500,
    )

    price = models.FloatField()

    image = models.ImageField(
        upload_to='photos/products',
    )

    stock = models.IntegerField(
        validators=(MinValueValidator(0),),
    )

    is_available = models.BooleanField(
        default=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    modified_date = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):
    VARIATION_CATEGORY_CHOICES = (
        ('color', 'color'),
        ('size', 'size'),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    variation_category = models.CharField(
        max_length=100,
        choices=VARIATION_CATEGORY_CHOICES,
    )

    variation_value = models.CharField(
        max_length=100,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_date = models.DateTimeField(
        auto_now=True
    )

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product,
        default=None,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to='store/products',
        max_length=255,
    )

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name_plural = 'Product Gallery'


class WishList(models.Model):
    owner = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    added_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.product.product_name
