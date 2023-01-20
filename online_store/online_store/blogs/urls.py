from django.urls import path

from online_store.blogs.views import BlogView, BlogDetailView, DeleteBlogView

urlpatterns = (
    path('', BlogView.as_view(), name='blog'),
    path('details/<int:pk>', BlogDetailView.as_view(), name='blog_details'),
    path('delete_blog/<int:pk>/', DeleteBlogView.as_view(), name='delete_blog'),
)
