from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from online_store.helpers import BootstrapFormMixin


UserModel = get_user_model()


class UserRegistrationForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('name', 'email', 'password1', 'password2')
