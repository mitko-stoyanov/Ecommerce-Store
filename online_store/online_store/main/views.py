from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from online_store.accounts.models import AppUser
from online_store.carts.models import Cart
from online_store.contacts.models import Contact
from online_store.helpers import BootstrapFormMixin
from online_store.main.forms import ChangePasswordForm
from online_store.orders.models import Order, OrderProduct
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


class ProfilePageView(BootstrapFormMixin, TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        orders = Order.objects.filter(user=user).order_by('-pk')
        total_orders = Order.objects.all()
        total_users = AppUser.objects.all()
        users_messages = Contact.objects.all().order_by('-pk')
        products_count = Product.objects.all().count()

        context['user'] = user
        context['orders'] = orders
        context['total_orders'] = total_orders
        context['products_count'] = products_count
        context['total_orders_count'] = total_orders.count()
        context['total_users'] = total_users
        context['total_users_count'] = total_users.count()
        context['messages'] = users_messages
        return context


class EditProfileView(UpdateView):
    model = AppUser
    fields = ('username',)


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'profile/change_password.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Паролата беше променена успешно.')
        return super().form_valid(form)


class ChangeOrderStatus(UpdateView):
    model = Order
    fields = ['status']
    template_name = 'orders/change_status.html'
    success_url = reverse_lazy('profile')

