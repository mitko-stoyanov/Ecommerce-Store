from django.urls import path

from online_store.orders.views import PlaceOrderView, OrderPreview

urlpatterns = (
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('order_preview/<int:pk>/', OrderPreview.as_view(), name='order_preview')
)