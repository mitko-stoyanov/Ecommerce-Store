from django.contrib import admin

from online_store.accounts.models import AppUser


@admin.register(AppUser)
class UserAdmin(admin.ModelAdmin):
    pass