from django.urls import path

from . import views
from .views import CartListView

urlpatterns = (
    path('', CartListView.as_view(), name='cart_page'),
    path('add/<int:pk>/', views.add_to_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
)