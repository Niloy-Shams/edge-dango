from django.contrib import admin
from django.db.models import Count
from . import models

# Register your models here.

admin.site.register(models.Customer)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'collection_title', 'inventory_status', 'promotions_count']
    list_editable = ['price']
    ordering = ['title']
    list_select_related = ['collection']
    list_per_page = 10
    search_fields = ['title']
    
    @admin.display(ordering='collection__title')
    def collection_title(self, product):
        return product.collection.title

    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            promotions_count=Count('promotions')
        )
        
    @admin.display(ordering='promotions_count')
    def promotions_count(self, product):
        return product.promotions_count
    

admin.site.register(models.Category)
admin.site.register(models.Collection)
admin.site.register(models.Promotion)
admin.site.register(models.Address)
