from django.contrib import admin

from online_store.orders.models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'phone', 'city', 'address', 'order_total', 'created_at', 'status')
    list_editable = ('status',)
    search_fields = ('order_number', 'email', 'phone',)
    inlines = [OrderProductInline]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'product_price', 'ordered')
