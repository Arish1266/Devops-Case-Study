from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    # Checkout Process
    path('', views.checkout_process, name='checkout'),
    
    # Order Confirmation
    path('order/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),
    
    # Order History
    path('history/', views.order_history, name='order_history'),
    
    # Apply Coupon (AJAX)
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]