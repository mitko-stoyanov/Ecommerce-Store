from django.contrib.auth import login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView

from online_store.accounts.forms import UserRegistrationForm, UserLoginForm
from online_store.accounts.models import AppUser
from online_store.accounts.tokens import AccActivateToken, token_generator
from online_store.helpers import BootstrapFormMixin


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()

        current_site = get_current_site(self.request)
        subject = 'Активирай своя акаунт в MaleFashion'
        message = render_to_string('authentication/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        })

        to_email = user.email
        send_email = EmailMessage(subject, message, to=[to_email])
        send_email.send()

        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy('home')


def activate(request, uidb64, token):
    User = get_user_model()

    try:
        uid = int(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('about')
    else:
        return redirect('register')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
