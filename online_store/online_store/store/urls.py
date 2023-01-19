from django.urls import path

from online_store.store.views import StorePageView, SearchPageView, ShowDetails, add_to_wish, WishListView, \
    delete_from_wish

urlpatterns = (
    path('', StorePageView.as_view(), name='store'),
    path('category/<slug:category_slug>', StorePageView.as_view(), name='products_by_category'),
    path('search/', SearchPageView.as_view(), name='search'),
    path('product-details/<int:pk>', ShowDetails.as_view(), name='product_details'),
    path('wish_list/', WishListView.as_view(), name='wish_list'),
    path('add_to_wish/<int:pk>', add_to_wish, name='add_to_wish'),
    path('remove_from_wish/<int:pk>', delete_from_wish, name='remove_from_wish'),
)
