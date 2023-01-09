import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from online_store.carts.models import CartItem
from online_store.orders.forms import OrderForm
from online_store.orders.models import Order


def make_order_num():
    year = int(datetime.date.today().strftime('%Y'))
    date = int(datetime.date.today().strftime('%d'))
    month = int(datetime.date.today().strftime('%m'))
    result = datetime.date(year, month, date)
    current_date = result.strftime('%Y%m%d')

    return current_date


class PlaceOrderView(CreateView):
    form_class = OrderForm
    model = Order
    template_name = 'store/checkout.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        current_order = form.save(commit=False)

        products = [p for p in CartItem.objects.all() if p.cart == self.request.user.cart]
        total = sum([(c.product.price * c.quantity) for c in products])

        current_order.user = self.request.user
        current_order.order_total = total
        current_order.ip = self.request.META.get('REMOTE_ADDR')
        current_order.save()

        order_number = make_order_num() + str(form.instance.pk)
        current_order.order_number = order_number
        current_order.save()

        return super(PlaceOrderView, self).form_valid(form)
