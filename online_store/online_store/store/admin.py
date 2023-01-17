from django.contrib import admin

from online_store.store.models import Category, Product, Variation, ProductGallery
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('category_name',)
    }

    list_display = ('category_name', 'slug')


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('product_name',)
    }

    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    inlines = [ProductGalleryInline, VariationInline]


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product',)


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    pass
