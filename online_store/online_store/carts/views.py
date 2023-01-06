from django.shortcuts import redirect
from django.views.generic import ListView

from online_store.carts.models import Cart, CartItem
from online_store.store.models import Product


class CartListView(ListView):
    model = CartItem
    template_name = 'store/cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = [p for p in CartItem.objects.all() if p.cart == self.request.user.cart]
        return products

    def get_context_data(self, **kwargs):
        total = 0
        products = [p for p in CartItem.objects.all() if p.cart == self.request.user.cart]
        for cart_item in products:
            total += (cart_item.product.price * cart_item.quantity)

        context = super(CartListView, self).get_context_data(**kwargs)
        context['total'] = total
        return context


def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    try:
        cart = Cart.objects.get(owner__exact=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            owner=request.user,
        )

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart_page')
