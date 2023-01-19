from django.shortcuts import render
from django.views.generic import ListView, DetailView

from online_store.blogs.models import Blog


# Create your views here.

class BlogView(ListView):
    model = Blog
    template_name = 'blogs/blog.html'
    context_object_name = 'blogs'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_details.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        current_pk = self.get_object().pk
        try:
            context['next_blog'] = Blog.objects.get(pk=current_pk + 1)
        except:
            pass

        try:
            context['previous_blog'] = Blog.objects.get(pk=current_pk - 1)
        except:
            pass

        return context
