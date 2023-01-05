from django.urls import path

from online_store.store.views import StorePageView, SearchPageView, ShowDetails

urlpatterns = (
    path('', StorePageView.as_view(), name='store'),
    path('category/<slug:category_slug>', StorePageView.as_view(), name='products_by_category'),
    path('search/', SearchPageView.as_view(), name='search'),
    path('product-details/<int:pk>', ShowDetails.as_view(), name='product_details')
)