from django.urls import path

from online_store.contacts.views import ShowContactPage, DeleteMessageView

urlpatterns = (
    path('', ShowContactPage.as_view(), name='contact'),
    path('delete_message/<int:pk>/', DeleteMessageView.as_view(), name='delete_message'),
)
