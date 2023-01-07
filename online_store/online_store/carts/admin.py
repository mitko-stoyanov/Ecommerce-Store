from django.contrib import admin

from online_store.carts.models import Cart, CartItem, Discount


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date_added')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('owner', 'code', 'discount_percent', 'times_used')
    readonly_fields = ('times_used',)
