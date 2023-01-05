from django.contrib import admin

from online_store.carts.models import Cart


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date_added')