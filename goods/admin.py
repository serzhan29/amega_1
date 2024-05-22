from django.contrib import admin
from django.utils.safestring import mark_safe
from goods.models import Categories, Products, SubCategories
from django.utils.html import format_html



@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_image']
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        else:
            return 'Нет фото'

    display_image.short_description = 'Изображение'


@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_image', 'category']
    prepopulated_fields = {'slug': ('name',)}

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        else:
            return 'Нет фото'

    display_image.short_description = 'Изображение'


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["get_image", "name", "quantity", "price", "discount"]
    list_display_links = ["get_image", "name",]
    list_editable = ["discount",]
    search_fields = ["name", "description"]
    list_filter = ["discount", "quantity", "category"]
    fields = [
        "name",
        "category",
        "sub_category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
    ]

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100">')
        else:
            return ""

    get_image.short_description = "Изображение"