from django.views.generic import TemplateView

from online_store.store.models import Product, Category


class StorePageView(TemplateView):
    def get_context_data(self, **kwargs):
        if kwargs and kwargs['category_slug'] is not None:
            products = Product.objects.filter(category__slug__iexact=kwargs['category_slug'], is_available=True)
        else:
            products = Product.objects.filter(is_available=True)

        categories = Category.objects.all()

        super().get_context_data(**kwargs)
        context = {
            'products': products,
            'result_count': products.count(),
            'total_count': Product.objects.filter(is_available=True).count(),
            'categories': categories,
        }
        return context

    template_name = 'store/store.html'
