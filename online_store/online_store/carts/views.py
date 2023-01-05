from django.shortcuts import render, get_object_or_404, redirect

from online_store.carts.models import Cart, CartItem
from online_store.store.models import Product


# Create your views here.
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
    return redirect('home')
