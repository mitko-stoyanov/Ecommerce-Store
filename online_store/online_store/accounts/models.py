from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from online_store.accounts.managers import AppUsersManager


class AppUser(AbstractBaseUser):
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True,)
    date_joined = models.DateTimeField(auto_now_add=True,)
    is_active = models.BooleanField(default=False,)
    is_staff = models.BooleanField(default=False,)
    is_admin = models.BooleanField(default=False,)
    is_superadmin = models.BooleanField(default=False,)
    last_login = models.DateTimeField(auto_now_add=True,)

    USERNAME_FIELD = 'email'

    objects = AppUsersManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
