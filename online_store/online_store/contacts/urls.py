from django.urls import path

from online_store.contacts.views import ShowContactPage


urlpatterns = (
    path('', ShowContactPage.as_view(), name='contact'),
)