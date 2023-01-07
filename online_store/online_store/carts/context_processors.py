from online_store.carts.models import Cart, CartItem


def counter(request):
    cart_count = 0
    total = 0

    if 'admin' in request.path:
        # if we are in admin panel we don't need that context
        return {}
    else:
        try:
            cart = Cart.objects.get(owner__exact=request.user)
            cart_items = CartItem.objects.all().filter(cart=cart)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
                total += cart_item.product.price * cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
            total = 0

    result = {
        'cart_count': cart_count,
        'total': total
    }
    return result