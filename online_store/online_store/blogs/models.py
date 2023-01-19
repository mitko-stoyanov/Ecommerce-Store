from django.db import models

from online_store.accounts.models import AppUser


class Blog(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=150,
        unique=True,
    )

    image = models.ImageField(
        upload_to='photos/blogs',
    )

    description = models.TextField()

    added_on = models.DateField(
        auto_now_add=True,
    )

    updated_on = models.DateField(
        auto_now=True,
    )
