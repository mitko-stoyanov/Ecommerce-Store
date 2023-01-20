from django.contrib import admin

from online_store.contacts.models import Contact


# Register your models here.


@admin.register(Contact)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'subject', 'message', 'created_at',)
