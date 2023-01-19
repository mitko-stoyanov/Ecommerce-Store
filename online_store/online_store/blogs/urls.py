from django.urls import path

from online_store.blogs.views import BlogView

urlpatterns = (
    path('', BlogView.as_view(), name='blog'),
)
