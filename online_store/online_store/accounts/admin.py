from django.contrib import admin

from online_store.accounts.models import AppUser


@admin.register(AppUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'last_login', 'date_joined', 'is_active')
    readonly_fields = ('password',)