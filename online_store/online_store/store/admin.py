from django.contrib import admin

from online_store.store.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('category_name',)
    }

    list_display = ('category_name', 'slug')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('product_name',)
    }

    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
