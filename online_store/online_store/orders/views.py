import datetime

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from online_store.carts.models import CartItem
from online_store.orders.forms import OrderForm
from online_store.orders.models import Order, OrderProduct
from online_store.store.models import Product


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

    def get_success_url(self):
        return f'/orders/order_preview/{self.object.pk}'

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

    def get_context_data(self, **kwargs):
        context = super(PlaceOrderView, self).get_context_data(**kwargs)
        context['products'] = [p for p in CartItem.objects.all() if p.cart == self.request.user.cart]
        return context


class OrderPreview(TemplateView):
    template_name = 'store/order_preview.html'

    def get_context_data(self, **kwargs):
        context = super(OrderPreview, self).get_context_data(**kwargs)
        order_pk = kwargs.get('pk')
        cart_items = CartItem.objects.filter(cart__owner=self.request.user)

        if order_pk:
            current_order = Order.objects.get(pk=order_pk)
            context['order'] = current_order
            context['cart_items'] = cart_items
        return context


def move_products(request, pk):
    cart_items = CartItem.objects.filter(cart__owner=request.user)
    order = Order.objects.get(user=request.user, is_ordered=False, pk=pk)

    for item in cart_items:
        ordered_product = OrderProduct()
        ordered_product.order_id = order.id
        ordered_product.user_id = request.user.id
        ordered_product.product_id = item.product_id
        ordered_product.quantity = item.quantity
        ordered_product.product_price = item.product.price
        ordered_product.ordered = True
        ordered_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        ordered_product = OrderProduct.objects.get(id=ordered_product.id)
        ordered_product.variations.set(product_variation)
        ordered_product.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(cart__owner=request.user).delete()

    subject = 'Thank you for your order'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()

    return redirect('home')
