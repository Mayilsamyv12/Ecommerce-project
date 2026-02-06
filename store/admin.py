from django.contrib import admin
from .models import Products, Category, Customer, Order, ProductImage, Feedback
from django.utils.html import format_html

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class AdminProduct(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Image'

    list_display = ['image_tag', 'name', 'price', 'category', 'description']
    list_filter = ['category']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    search_fields = ['first_name', 'last_name', 'email', 'phone']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'quantity', 'price', 'date', 'status', 'delivery_status']
    list_filter = ['delivery_status', 'date']
    search_fields = ['product__name', 'customer__first_name', 'address', 'phone']
    actions = ['mark_as_shipped', 'mark_as_out_for_delivery', 'mark_as_delivered']

    def mark_as_shipped(self, request, queryset):
        queryset.update(delivery_status='Shipped')
    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    def mark_as_out_for_delivery(self, request, queryset):
        queryset.update(delivery_status='Out For Delivery')
    mark_as_out_for_delivery.short_description = "Mark selected orders as Out For Delivery"

    def mark_as_delivered(self, request, queryset):
        queryset.update(delivery_status='Delivered', status=True)
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'customer__email']

# Register your models here.
admin.site.register(Products, AdminProduct)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Feedback, FeedbackAdmin)


# username = Tanushree, email = tanushree7252@gmail.com, password = 1234
