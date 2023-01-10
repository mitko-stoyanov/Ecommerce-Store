from django.contrib import admin

from online_store.orders.models import Payment, Order, OrderProduct


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'city', 'address', 'order_number', 'order_total', 'created_at')
    search_fields = ('order_number',)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    pass
