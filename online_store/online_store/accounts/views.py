from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView

from online_store.accounts.forms import UserRegistrationForm, UserLoginForm, ForgotPasswordForm, ResetPasswordForm
from online_store.accounts.models import AppUser
from online_store.accounts.utils import send_email
from online_store.carts.models import Cart


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('home')
    success_message = 'Профилът е създаден успешно. Изпратили сме ви имейл, чрез който да го активирате.'

    def form_valid(self, form):
        user = form.save()

        subject = 'Активирай своя акаунт в MaleFashion'
        path = 'authentication/activation_email.html'
        send_email(self.request, user, subject, path)

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
