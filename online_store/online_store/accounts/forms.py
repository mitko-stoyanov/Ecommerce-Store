from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from online_store.helpers import BootstrapFormMixin

UserModel = get_user_model()


class UserRegistrationForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('name', 'email', 'password1', 'password2')


class UserLoginForm(BootstrapFormMixin, AuthenticationForm):
    pass


class ForgotPasswordForm(BootstrapFormMixin, forms.Form):
    email = forms.EmailField(
        max_length=100,
    )


class ResetPasswordForm(BootstrapFormMixin, forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())

    password2 = forms.CharField(widget=forms.PasswordInput())


