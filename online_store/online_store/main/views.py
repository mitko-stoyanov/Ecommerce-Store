from django.shortcuts import render
from django.views.generic import TemplateView

from online_store.store.models import Product


class HomePageView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        new_products = Product.objects.all().filter(is_available=True).order_by('-id')[:4]
        context = super().get_context_data(**kwargs)
        context['new_products'] = new_products
        return context



class AboutPageView(TemplateView):
    template_name = 'main/about.html'
