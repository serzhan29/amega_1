from django.contrib import admin
from django.utils.html import format_html
from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin

from users.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ["display_image","username", "first_name", "last_name", "email",]
    search_fields = ["username", "first_name", "last_name", "email"]
    list_display_links = ["display_image", "username"]

    inlines = [CartTabAdmin, OrderTabulareAdmin]

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50"/>'.format(obj.image.url))
        else:
            return 'Нет Фото'

    display_image.allow_tags = True
    display_image.short_description = 'Фото пользователя'

admin.site.register(User, UserAdmin)
