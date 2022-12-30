from django.urls import path

from online_store.accounts import views
from online_store.accounts.views import UserRegistrationView, UserLogoutView, UserLoginView

urlpatterns = (
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
)