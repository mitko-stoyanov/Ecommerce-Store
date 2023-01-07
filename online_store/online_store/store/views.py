from itertools import chain

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from online_store.store.models import Product, Category


class ShowDetails(DetailView):
    model = Product
    template_name = 'store/product_details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ShowDetails, self).get_context_data(**kwargs)
        related_products = Product.objects.filter(category=self.get_object().category).exclude(pk=self.get_object().pk)
        context['related_products'] = related_products
        return context


class StorePageView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'
    paginate_by = 2

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
