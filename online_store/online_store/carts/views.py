from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView

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
        total_without_disc = 0
        products = [p for p in CartItem.objects.all() if p.cart == self.request.user.cart]
        total_without_disc = sum([(c.product.price * c.quantity) for c in products])
        context = super(CartListView, self).get_context_data(**kwargs)
        context['total_without_disc'] = total_without_disc
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


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(owner__exact=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart_page')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(owner__exact=request.user)
    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass

    return redirect('cart_page')
