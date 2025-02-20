from django.core.management.base import BaseCommand
from django.db import transaction
from store.models import Category, Product, Customer, Collection, Promotion

class Command(BaseCommand):
    help = 'Clears all data from the database'

    @transaction.atomic
    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()
        Collection.objects.all().delete()
        Customer.objects.all().delete()
        Promotion.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Successfully cleared all data from database'))