from rest_framework import serializers
from decimal import Decimal
from .models import Product
from .models import Collection

class ProductSerializer(serializers.ModelSerializer):
    
    tax = serializers.SerializerMethodField()
    collection = serializers.StringRelatedField(read_only=True)
    collection_id = serializers.IntegerField(required=True, write_only=True)
    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.IntegerField(required=True, write_only=True)
    
    def get_tax(self, product):
        return product.price * Decimal('0.1')
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'collection', 'collection_id', 'category', 'category_id', 'tax', 'inventory']
    
    # Custom validation -> Object level (Product)
    def validate(self, data):
        if data['inventory'] < 1:
            raise serializers.ValidationError('Inventory must be at least 1')
        return data
    
    # Custom validation -> Field level (Price of the product)
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value