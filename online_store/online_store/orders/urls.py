from django.urls import path

from online_store.orders.views import PlaceOrderView, OrderPreview, move_products, OrderCompleteView, WrongOrderInfoView

urlpatterns = (
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('order_preview/<int:pk>/', OrderPreview.as_view(), name='order_preview'),
    path('delete_order/<int:pk>/', WrongOrderInfoView.as_view(), name='delete_order'),
    path('make_order/<int:pk>/', move_products, name='make_order'),
    path('complete/<int:pk>/', OrderCompleteView.as_view(), name='complete'),
)