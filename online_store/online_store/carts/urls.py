from django.urls import path

from . import views
from online_store.store.views import StorePageView, SearchPageView, ShowDetails

urlpatterns = (
    path('add/<int:pk>/', views.add_to_cart, name='cart'),
)