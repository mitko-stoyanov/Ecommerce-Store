from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from online_store.carts.models import Cart, CartItem
from online_store.store.models import Product, Variation


def find_cart_products(self):
    user_cart = self.request.user.cart
    products = [p for p in CartItem.objects.all() if p.cart == user_cart]
    return products


class CartListView(ListView):
    model = CartItem
    template_name = 'store/cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = find_cart_products(self)
        return products

    def get_context_data(self, **kwargs):
        total_without_disc = 0
        products = find_cart_products(self)
        total_without_disc = sum([(c.product.price * c.quantity) for c in products])
        context = super().get_context_data(**kwargs)
        context['total_without_disc'] = total_without_disc
        return context


def add_to_cart(request, pk):
    product = Product.objects.get(pk=pk)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    cart = Cart.objects.get(owner__exact=request.user)

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
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

    cart_item = get_object_or_404(CartItem, product=product, cart=cart, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart_page')
