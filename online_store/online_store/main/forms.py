from django.contrib.auth.forms import PasswordChangeForm
from django import forms

from online_store.helpers import BootstrapFormMixin
from online_store.orders.models import Order


class ChangePasswordForm(BootstrapFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()


class ChangeOrderStatusForm(forms.Form):
    class Meta:
        model = Order
        fields = ('status',)
