from django.core.management.base import BaseCommand
import requests
from store.models import ProductCategory, Product


class Command(BaseCommand):
    help = 'Populates the database with data from Fake Store API'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate database from Fake Store API')

        # Fetch categories
        categories_response = requests.get('https://fakestoreapi.com/products/categories')
        categories = categories_response.json()

        for category_name in categories:
            category, created = ProductCategory.objects.get_or_create(title=category_name)
            if created:
                self.stdout.write(f'Added new category: {category.title}')

        # Fetch products
        products_response = requests.get('https://fakestoreapi.com/products')
        products = products_response.json()

        for product_data in products:
            category_title = product_data['category']
            category = ProductCategory.objects.get(title=category_title)

            product, created = Product.objects.get_or_create(
                title=product_data['title'],
                defaults={
                    'category': category,
                    'price': product_data['price'],
                    'description': product_data['description'],
                    'image': product_data['image'],
                    # Set default values for average_rating and rating_count
                    'average_rating': 0,
                    'rating_count': 0
                }
            )
            if created:
                self.stdout.write(f'Added new product: {product.title}')

        self.stdout.write('Database population complete')
