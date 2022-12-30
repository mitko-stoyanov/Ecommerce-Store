from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_store.main.urls')),
    path('authentication/', include('online_store.accounts.urls')),
]
