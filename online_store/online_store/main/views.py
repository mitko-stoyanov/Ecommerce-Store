from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from online_store.accounts.models import AppUser
from online_store.carts.models import Cart
from online_store.store.models import Product


class HomePageView(SuccessMessageMixin, TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            user = self.request.user
            if user and not Cart.objects.filter(owner__exact=user).exists():
                messages.info(self.request,
                              'Количката ще се появи в горния десен ъгъл след като добавите първия си продукт.')
        except:
            pass

        new_products = Product.objects.all().filter(is_available=True).order_by('-id')[:4]
        context['new_products'] = new_products
        return context


class AboutPageView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        clients = AppUser.objects.all().count()
        products = Product.objects.all().count()

        context = {
            'clients_count': clients,
            'products_count': products,
        }

        return context
