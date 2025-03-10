from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Wishlist, ProductReview

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        category_slug = self.kwargs.get('category_slug')
        search_query = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort', 'name')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created')
        else:
            queryset = queryset.order_by('name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort', 'name')
        if self.request.user.is_authenticated:
            context['wishlist_products'] = Wishlist.objects.filter(
                user=self.request.user
            ).values_list('products__id', flat=True)
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.all().order_by('name')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        if self.request.user.is_authenticated:
            context['in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user,
                products=self.object
            ).exists()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.filter(available=True)
        return context
        
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.add_product(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'added'})
    
    messages.success(request, f'{product.name} has been added to your wishlist.')
    return redirect('products:product_detail', product.slug)

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.remove_product(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed'})
    
    messages.success(request, f'{product.name} has been removed from your wishlist.')
    return redirect('products:product_detail', product.slug)

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist': wishlist})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Update or create review
        review, created = ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        messages.success(request, 'Your review has been submitted.')
        return redirect('products:product_detail', product.slug)
    
    return redirect('products:product_detail', product.slug)
