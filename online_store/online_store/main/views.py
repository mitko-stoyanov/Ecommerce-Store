from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from online_store.accounts.models import AppUser
from online_store.blogs.models import Blog
from online_store.contacts.models import Contact
from online_store.main.forms import ChangePasswordForm
from online_store.orders.models import Order
from online_store.store.models import Product


class HomePageView(SuccessMessageMixin, TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        new_products = Product.objects.all().filter(is_available=True).order_by('-id')[:4]
        last_blogs = Blog.objects.all()[:3]

        context = {
            'last_blogs': last_blogs,
            'new_products': new_products
        }
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


class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        orders = Order.objects.filter(user=user).order_by('-pk')
        total_orders = Order.objects.all()
        total_users = AppUser.objects.all()
        users_messages = Contact.objects.all().order_by('-pk')
        products_count = Product.objects.all().count()
        blogs = Blog.objects.all()

        context = {
            'user': user,
            'orders': orders,
            'total_orders': total_orders,
            'total_orders_count': total_orders.count(),
            'products_count': products_count,
            'total_users': total_users,
            'total_users_count': total_users.count(),
            'total_blogs': blogs,
            'total_blogs_count': blogs.count(),
            'messages': users_messages
        }

        return context


class EditProfileView(UpdateView):
    model = AppUser
    fields = ('username',)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'profile/change_password.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Паролата беше променена успешно.')
        return super().form_valid(form)


class ChangeOrderStatus(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['status']
    template_name = 'orders/change_status.html'
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request,
                           'Тази страница е достъпна само от администратори. '
                           'Ако мислите, че сме допуснали грешка - свържете се с нас')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
