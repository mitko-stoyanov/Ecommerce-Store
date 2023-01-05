from django.contrib.auth import get_user_model
from django.db import models


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
