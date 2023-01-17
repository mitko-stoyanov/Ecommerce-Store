from django.urls import path

from online_store.main.views import HomePageView, AboutPageView, ProfilePageView, ChangePasswordView, ChangeOrderStatus

urlpatterns = (
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('profile/change_pasword/', ChangePasswordView.as_view(), name='change_password'),
    path('update_order/<int:pk>/', ChangeOrderStatus.as_view(), name='update_order'),
)
