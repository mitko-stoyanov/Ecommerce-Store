from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from online_store.contacts.forms import ContactForm
from online_store.contacts.models import Contact


class ShowContactPage(CreateView):
    template_name = 'contacts/contact.html'
    form_class = ContactForm
    model = Contact
    success_url = reverse_lazy('home')
