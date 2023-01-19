from django.contrib import admin

from online_store.blogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'image',)
    list_display = ('user', 'title', 'description', 'updated_on', 'added_on')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)
