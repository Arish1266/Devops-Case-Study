from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    def get_average_rating(self):
        if self.reviews.exists():
            return sum(review.rating for review in self.reviews.all()) / self.reviews.count()
        return 0

class ProductReview(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f'Review by {self.user} on {self.product}'

class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Wishlist for {self.user.username}"
    
    def add_product(self, product):
        """Add a product to the wishlist"""
        if not self.products.filter(id=product.id).exists():
            self.products.add(product)
    
    def remove_product(self, product):
        """Remove a product from the wishlist"""
        self.products.remove(product)
