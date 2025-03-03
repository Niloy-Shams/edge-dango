from django.core.management.base import BaseCommand
from faker import Faker
from store.models import Address, Category, Product, Customer, Collection, Promotion, Review
import random

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def handle(self, *args, **options):
        fake = Faker()
        
        # Create collections
        collections = []
        for _ in range(5):
            collection = Collection.objects.create(
                title=fake.word().title()
            )
            collections.append(collection)

        # Create categories
        categories = []
        for _ in range(10):
            category = Category.objects.create(
                name=fake.word().title()
            )
            categories.append(category)

        # Create promotions
        promotions = []
        for _ in range(3):
            promotion = Promotion.objects.create(
                description=fake.sentence()
            )
            promotions.append(promotion)

        # Create products
        for _ in range(50):
            product = Product.objects.create(
                title=fake.catch_phrase(),
                description=fake.text(),
                price=random.uniform(10.0, 1000.0),
                inventory=random.randint(0, 100),
                collection=random.choice(collections),
                category=random.choice(categories),
                last_update=fake.date_time_this_year(before_now=True, after_now=False),
            )
            # Add random promotions
            product.promotions.add(*random.sample(promotions, k=random.randint(0, 2)))

        # Create customers with addresses
        for _ in range(20):
            customer = Customer.objects.create(
                first_name=fake.first_name()
            )
            # Create exactly one address for each customer (OneToOneField)
            Address.objects.create(
                street=fake.street_address(),
                city=fake.city(),
                customer=customer
            )
            
        # Create reviews
        for product in Product.objects.all():
            for _ in range(random.randint(0, 10)):
                Review.objects.create(
                    rating=random.randint(1, 5),
                    description=fake.paragraph(),
                    product=product
                )
                

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))