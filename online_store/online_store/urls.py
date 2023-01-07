from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_store.main.urls')),
    path('authentication/', include('online_store.accounts.urls')),
    path('store/', include('online_store.store.urls')),
    path('cart/', include('online_store.carts.urls')),
    path('orders/', include('online_store.orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
