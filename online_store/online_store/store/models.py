from django.db import models
from django.urls import reverse


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

    stock = models.IntegerField()

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
