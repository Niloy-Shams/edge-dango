from django.db import models

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.description
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    # Forward reference using string
    featured_product = models.ForeignKey(
        'Product',  # Using string because Product isn't defined yet
        on_delete=models.SET_NULL,
        null=True,
        related_name='+'  # No reverse relationship
    )
    
    def __str__(self):
        return self.name

class Product(models.Model):
    # Auto-created id field unless primary_key=True on another field
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,  # Total number of digits
        decimal_places=2  # Digits after decimal
    )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT  # Can't delete collection if it has products
    )
    promotions = models.ManyToManyField(
        Promotion,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.first_name

class Address(models.Model):
    # One customer can have only one address and vice versa
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,  # Delete address when customer is deleted
        primary_key=True  # Address ID will be same as Customer ID
    )
    
    def __str__(self):
        return self.city+','+self.street
    
class Review(models.Model):
    rating = models.IntegerField()
    description = models.TextField()
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return str(self.rating)
