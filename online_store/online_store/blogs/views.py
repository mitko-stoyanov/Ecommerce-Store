from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from online_store.blogs.models import Blog


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
        next_blog = Blog.objects.filter(pk=current_pk + 1).first()
        if next_blog:
            context['next_blog'] = next_blog

        previous_blog = Blog.objects.filter(pk=current_pk - 1).first()
        if previous_blog:
            context['previous_blog'] = previous_blog

        return context


class DeleteBlogView(DeleteView):
    model = Blog
    success_url = reverse_lazy('profile')
