from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView

from online_store.carts.models import CartItem
from online_store.orders.forms import OrderForm
from online_store.orders.models import Order, OrderProduct
from online_store.orders.utils import make_order_num
from online_store.store.models import Product

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.core.mail import send_mail


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

    subject = 'Благодарим за направената поръчка'
    message = render_to_string('orders/order_received_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(subject, message, to=[to_email])
    send_email.send()

    return redirect('complete', pk=order.pk)


class OrderCompleteView(TemplateView):
    template_name = 'orders/order_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order_pk = self.kwargs['pk']
        order = Order.objects.get(pk=order_pk)
        ordered_products = OrderProduct.objects.filter(order=order, user=self.request.user)

        context['order'] = order
        context['ordered_products'] = ordered_products

        return context


class WrongOrderInfoView(DeleteView):
    model = Order
    success_url = reverse_lazy('cart_page')


# @receiver(pre_save, sender=Order)
# def my_callback(sender, instance, **kwargs):
#     try:
#         old_instance = Order.objects.get(pk=instance.pk)
#     except Order.DoesNotExist:
#         pass
#     else:
#         if old_instance.status != instance.status:
#             message = render_to_string('orders/changed_status_email.html',
#                                        {
#                                            'order': instance,
#                                        })
#             send_mail(
#                 'Статусът е променен',
#                 message,
#                 None,
#                 [old_instance.user.email],
#             )


class DeleteOrderView(DeleteView):
    model = Order
    success_url = reverse_lazy('profile')
