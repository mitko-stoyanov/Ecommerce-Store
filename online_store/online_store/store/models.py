from django.db import models


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
