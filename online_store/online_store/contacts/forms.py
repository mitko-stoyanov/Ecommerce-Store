from django import forms

from online_store.contacts.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('email', 'subject', 'message')

        widgets = {
            'email': forms.TextInput(
                attrs={'placeholder': 'Имейл адрес'}
            ),
            'subject': forms.TextInput(
                attrs={'placeholder': 'Заглавие'}
            ),
            'message': forms.Textarea(
                attrs={'placeholder': 'Съобщение'}
            )
        }
