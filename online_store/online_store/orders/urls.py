from django.urls import path

from online_store.orders.views import PlaceOrderView, OrderPreview, move_products, OrderCompleteView, \
    WrongOrderInfoView, DeleteOrderView

urlpatterns = (
    path('place_order/', PlaceOrderView.as_view(), name='place_order'),
    path('order_preview/<int:pk>/', OrderPreview.as_view(), name='order_preview'),
    path('delete_order/<int:pk>/', WrongOrderInfoView.as_view(), name='delete_order'),
    path('delete_order_profile/<int:pk>/', DeleteOrderView.as_view(), name='delete_order_profile'),
    path('make_order/<int:pk>/', move_products, name='make_order'),
    path('complete/<int:pk>/', OrderCompleteView.as_view(), name='complete'),
)