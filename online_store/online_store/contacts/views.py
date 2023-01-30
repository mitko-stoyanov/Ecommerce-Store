from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.contrib import messages

from online_store.contacts.forms import ContactForm
from online_store.contacts.models import Contact


class ShowContactPage(SuccessMessageMixin, CreateView):
    template_name = 'contacts/contact.html'
    form_class = ContactForm
    model = Contact
    success_url = reverse_lazy('home')
    success_message = 'Успешно изпратихте своето запитване. Очаквайте отговор на посочения имейл в най-кратки срокове.'


class DeleteMessageView(DeleteView):
    model = Contact
    success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request,
                           'Тази страница е достъпна само от администратори. '
                           'Ако мислите, че сме допуснали грешка - свържете се с нас')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
