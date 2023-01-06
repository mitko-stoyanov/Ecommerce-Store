from django.urls import path

from . import views
from .views import CartListView

urlpatterns = (
    path('', CartListView.as_view(), name='cart_page'),
    path('add/<int:pk>/', views.add_to_cart, name='add_cart'),
)