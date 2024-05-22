import matplotlib.pyplot as plt
import io
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib import admin
from orders.models import Order, OrderItem
from django.utils.html import format_html
from django.urls import path  # Add this line
from django.utils.html import format_html


class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = ("product", "name", "price", "quantity")
    search_fields = ("product", "name")
    extra = 0


# ---------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product_image","order", "product", "name", "price", "quantity", "total_sales",)
    search_fields = ("order", "product", "name")

    def product_image(self, obj):
        if obj.product and obj.product.image:
            return format_html('<img src="{}" width="50" height="50"/>'.format(obj.product.image.url))
        else:
            return 'Нет фото'

    product_image.allow_tags = True
    product_image.short_description = 'Фото продукта'

    def total_sales(self, obj):
        return f" {obj.price * obj.quantity} ₸"

    total_sales.short_description = 'Общая сумма'

    def sales_chart(self, request):
        sales_data = (
            OrderItem.objects
            .values('product__name')
            .annotate(total_quantity=Sum('quantity'), total_sales=Sum('price'))
        )

        products = [item['product__name'] for item in sales_data]
        quantities = [item['total_quantity'] for item in sales_data]

        fig, ax = plt.subplots()
        ax.bar(products, quantities)
        ax.set_xlabel('Product')
        ax.set_ylabel('Quantity Sold')
        ax.set_title('Product Sales Quantity')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot to a temporary buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Return the buffer content as the HTTP response
        response = HttpResponse(buffer, content_type='image/png')
        return response

        sales_chart.short_description = 'Sales Chart'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('sales-chart/', self.admin_site.admin_view(self.sales_chart), name='sales_chart'),
        ]
        return my_urls + urls

# ----------------
class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = ("requires_delivery", "status", "payment_on_get", "is_paid", "created_timestamp")
    search_fields = ("user", "requires_delivery", "payment_on_get", "is_paid", "created_timestamp")
    readonly_fields = ("created_timestamp",)
    extra = 0


""" Заказы """
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "product_image", "id", "user", "user_image", "requires_delivery", "status", "status_2",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    list_display_links = ("id", "user")
    search_fields = ("id", "user")
    readonly_fields = ("created_timestamp",)
    list_filter = ("user", "requires_delivery", "status", "payment_on_get", "is_paid", "status_2")
    inlines = (OrderItemTabulareAdmin,)

    def product_image(self, obj):
        order_items = obj.orderitem_set.all()
        if order_items.exists():
            first_order_item = order_items.first()
            if first_order_item.product and first_order_item.product.image:
                return format_html('<img src="{}" width="50" height="50"/>'.format(first_order_item.product.image.url))
        return 'No Image'

    product_image.allow_tags = True
    product_image.short_description = 'Фото продукта'

    def user_image(self, obj):
        if obj.user.image:
            return format_html('<img src="{}" width="50" height="50"/>'.format(obj.user.image.url))
        else:
            return 'Нет фото'

    user_image.allow_tags = True
    user_image.short_description = 'Фото пользователя'
