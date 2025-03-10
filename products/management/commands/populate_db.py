from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
from faker import Faker
import random

fake = Faker()

CATEGORIES = [
    {
        'name': 'Laptops',
        'description': 'Powerful and portable computing devices'
    },
    {
        'name': 'Smartphones',
        'description': 'Latest mobile devices and accessories'
    },
    {
        'name': 'Audio',
        'description': 'Headphones, speakers, and audio equipment'
    },
    {
        'name': 'Gaming',
        'description': 'Gaming consoles and accessories'
    },
    {
        'name': 'Cameras',
        'description': 'Digital cameras and photography equipment'
    }
]

PRODUCTS = [
    # Laptops
    {
        'category': 'Laptops',
        'products': [
            {
                'name': 'MacBook Pro 14"',
                'price': 1999.99,
                'description': 'Apple M2 Pro chip, 16GB RAM, 512GB SSD'
            },
            {
                'name': 'Dell XPS 15',
                'price': 1799.99,
                'description': 'Intel i9, 32GB RAM, 1TB SSD, RTX 3050'
            },
            {
                'name': 'Lenovo ThinkPad X1',
                'price': 1599.99,
                'description': 'Intel i7, 16GB RAM, 512GB SSD'
            }
        ]
    },
    # Smartphones
    {
        'category': 'Smartphones',
        'products': [
            {
                'name': 'iPhone 14 Pro',
                'price': 999.99,
                'description': '6.1" Super Retina XDR display, A16 Bionic chip'
            },
            {
                'name': 'Samsung Galaxy S23',
                'price': 899.99,
                'description': '6.8" Dynamic AMOLED, Snapdragon 8 Gen 2'
            },
            {
                'name': 'Google Pixel 7',
                'price': 699.99,
                'description': '6.3" OLED display, Google Tensor G2'
            }
        ]
    },
    # Audio
    {
        'category': 'Audio',
        'products': [
            {
                'name': 'Sony WH-1000XM4',
                'price': 349.99,
                'description': 'Wireless Noise Cancelling Headphones'
            },
            {
                'name': 'AirPods Pro',
                'price': 249.99,
                'description': 'Active Noise Cancellation, Spatial Audio'
            },
            {
                'name': 'Sonos One',
                'price': 199.99,
                'description': 'Smart Speaker with Voice Control'
            }
        ]
    }
]

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Superuser created')

        # Create categories
        for cat_data in CATEGORIES:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        for cat_products in PRODUCTS:
            category = Category.objects.get(name=cat_products['category'])
            for prod_data in cat_products['products']:
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    defaults={
                        'category': category,
                        'description': prod_data['description'],
                        'price': prod_data['price'],
                        'stock': random.randint(10, 100),
                        'slug': fake.slug()
                    }
                )
                if created:
                    self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully'))