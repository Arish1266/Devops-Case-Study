from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product Listing and Search
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='category_products'),
    
    # Product Detail
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Wishlist Management
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Product Review
    path('review/add/<int:product_id>/', views.add_review, name='add_review'),
    
    path('category/<slug:category_slug>/detail/', views.CategoryDetailView.as_view(), name='category_detail'),
]