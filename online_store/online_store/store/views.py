from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from online_store.store.models import Product, Category, ProductGallery, WishList


class ShowDetails(DetailView):
    model = Product
    template_name = 'store/product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ShowDetails, self).get_context_data(**kwargs)
        related_products = Product.objects.filter(category=self.get_object().category).exclude(pk=self.get_object().pk)
        product_gallery = ProductGallery.objects.filter(product_id=self.object.id)
        context['category'] = self.get_object().category
        context['related_products'] = related_products
        context['product_gallery'] = product_gallery
        return context


class StorePageView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        if self.kwargs and self.kwargs['category_slug'] is not None:
            slug = self.kwargs['category_slug']
            products = Product.objects.filter(category__slug__iexact=slug, is_available=True)
        else:
            products = Product.objects.filter(is_available=True)

        return products.order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super(StorePageView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        context['total_count'] = Product.objects.filter(is_available=True).count()
        return context


class SearchPageView(StorePageView):
    paginate_by = 0

    def get_queryset(self):
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            if keyword:
                products = Product.objects.order_by('-created_date').filter(
                    Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).filter(is_available=True)
                return products


class WishListView(ListView):
    model = WishList
    template_name = 'store/wish_list.html'
    context_object_name = 'wish_products'

    def get_queryset(self):
        wish_list = WishList.objects.filter(owner=self.request.user)
        wish_products = [w.product for w in wish_list]
        return wish_products


def add_to_wish(request, pk):
    product = Product.objects.get(pk=pk)

    wish_list = WishList.objects.filter(owner=request.user)
    products = [w.product for w in wish_list]
    if product not in products:
        WishList.objects.create(
            owner=request.user,
            product=product
        )
        messages.success(request, f'Успешно добавихте {product.product_name} към вашия списък с желани артикули.')
    else:
        messages.error(request, 'Продуктът вече е добавен в списъка с желани артикули.')

    return redirect('store')


class DeleteFromWishView(DeleteView):
    model = WishList
    success_url = reverse_lazy('store')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, owner=self.request.user, product=Product.objects.get(pk=self.kwargs['pk']))
