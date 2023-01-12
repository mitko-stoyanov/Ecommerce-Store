from django import forms

from online_store.carts.models import CartItem
from online_store.orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'phone', 'order_note', 'city',)
