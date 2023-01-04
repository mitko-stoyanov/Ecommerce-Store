from django.urls import path

from online_store.store.views import StorePageView, SearchPageView

urlpatterns = (
    path('', StorePageView.as_view(), name='store'),
    path('category/<slug:category_slug>', StorePageView.as_view(), name='products_by_category'),
    path('search/', SearchPageView.as_view(), name='search'),
)