from django.contrib import admin
from .models import Order, OrderItem, Coupon

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'user', 
        'shipping_first_name', 
        'shipping_last_name', 
        'status', 
        'created_at'
    ]
    list_filter = [
        'status', 
        'created_at'
    ]
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 
        'discount', 
        'valid_from', 
        'valid_to', 
        'active'
    ]
    list_filter = [
        'active', 
        'valid_from', 
        'valid_to'
    ]
    search_fields = ['code']
