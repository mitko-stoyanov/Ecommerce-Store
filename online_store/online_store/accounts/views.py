from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, FormView

from online_store.accounts.forms import UserRegistrationForm, UserLoginForm, ForgotPasswordForm, ResetPasswordForm
from online_store.accounts.models import AppUser
from online_store.accounts.tokens import token_generator
from online_store.carts.models import Cart
from online_store.store.models import WishList


def send_email(request, user, subject_value, path):
    current_site = get_current_site(request)
    subject = subject_value
    message = render_to_string(path, {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    })

    to_email = user.email
    send_email = EmailMessage(subject, message, to=[to_email])
    return send_email.send()


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('home')
    success_message = 'Профилът е създаден успешно. Изпратили сме ви имейл, чрез който да го активирате.'

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

        response = super().form_valid(form)

        cart = Cart()
        cart.owner = self.object
        cart.save()

        return response


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
        messages.success(request, 'Успешно активирахте своя акаунт. Може да се логнете с имейл и парола.')
        return redirect('login')
    else:
        return redirect('register')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = AppUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, AppUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Успешно удостоверихте своя имейл. Моля изберете нова парола за акаунта.')
        return redirect('reset_password')
    else:
        messages.error(request, 'Тази връзка е изтекла. Моля опитайте отново!')
        return redirect('login')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class ForgotPasswordView(FormView):
    template_name = 'authentication/forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = 'authentication/login'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if AppUser.objects.filter(email=email).exists():
            user = AppUser.objects.get(email__exact=email)
            subject = 'Забравена парола'
            path = 'authentication/reset_password_email.html'
            send_email(self.request, user, subject, path)
            messages.success(self.request, 'Изпратихме ви имейл, чрез който трябва да удостоверите, че това сте вие.')
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(self.request, 'Моля въведете имейл, с който имате регистрация в сайта.')
            return HttpResponseRedirect(reverse('forgot_password'))


class ResetPasswordView(FormView):
    template_name = 'authentication/reset_password.html'
    form_class = ResetPasswordForm

    def form_valid(self, form):
        password = form.cleaned_data['password1']
        confirm_password = form.cleaned_data['password2']
        if password == confirm_password:
            uid = self.request.session.get('uid')
            user = AppUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(self.request, 'Паролата беше сменена успешно. Моля влезте с новите си данни')
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(self.request, 'Паролите не съвпадат, опитайте отново!')
            return HttpResponseRedirect(reverse('reset_password'))
