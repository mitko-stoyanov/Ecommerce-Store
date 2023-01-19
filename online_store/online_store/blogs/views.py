from django.shortcuts import render
from django.views.generic import ListView

from online_store.blogs.models import Blog


# Create your views here.

class BlogView(ListView):
    model = Blog
    template_name = 'blogs/blog.html'
    context_object_name = 'blogs'
