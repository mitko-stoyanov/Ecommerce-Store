from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from online_store.contacts.forms import ContactForm
from online_store.contacts.models import Contact


class ShowContactPage(SuccessMessageMixin, CreateView):
    template_name = 'contacts/contact.html'
    form_class = ContactForm
    model = Contact
    success_url = reverse_lazy('home')
    success_message = 'Успешно изпратихте своето запитване. Очаквайте отговор на посочения имейл в най-кратки срокове.'
