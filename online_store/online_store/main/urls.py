from django.urls import path

from online_store.main import views
from online_store.main.views import HomePageView

urlpatterns = (
    path('', HomePageView.as_view(), name='home'),
)