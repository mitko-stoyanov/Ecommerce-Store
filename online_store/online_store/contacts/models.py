from django.db import models

from online_store.accounts.models import AppUser


# Create your models here.

class Contact(models.Model):
    email = models.EmailField(
        max_length=60,
    )

    subject = models.CharField(
        max_length=30,
    )

    message = models.TextField(
        max_length=450,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
