from django.urls import path

from online_store.accounts import utils
from online_store.accounts.views import UserRegistrationView, UserLogoutView, UserLoginView, ForgotPasswordView, \
    ResetPasswordView

urlpatterns = (
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/', utils.activate, name='activate'),

    path('reset_password_validate/<uidb64>/<token>/', utils.reset_password_validate, name='reset_password_validate'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
)
