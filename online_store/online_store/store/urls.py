from django.urls import path

from online_store.store.views import StorePageView

urlpatterns = (
    path('', StorePageView.as_view(), name='store'),
    path('<slug:category_slug>', StorePageView.as_view(), name='products_by_category'),
)