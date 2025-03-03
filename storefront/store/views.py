from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Count, Max, Min, Avg, Case, When, Value, IntegerField
from store.models import Collection, Product
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CollectionSerializer, ProductSerializer, SimpleCollectoinSerializer
from rest_framework import status, viewsets

def product_list(request):
    return HttpResponse('Product List')

@api_view(['GET', 'POST'])
def product_list_drf(request):
    if request.method == 'GET':     
        # Add select_related to fetch related fields in a single query
        products = Product.objects\
            .select_related('collection', 'category')\
            .prefetch_related('promotions')\
            .all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_drf(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('collection'),
        pk=pk
    )
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        collections = Collection.objects.all()
        serializer = SimpleCollectoinSerializer(collections, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SimpleCollectoinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.prefetch_related, 
        pk=pk
    )
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SimpleCollectoinSerializer(instance=collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it has products.'}, 
                           status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionListClass(APIView):
    def get(self, request):
        collections = Collection.objects.all()
        serializer = SimpleCollectoinSerializer(collections, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = SimpleCollectoinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# Mixins and generics
from rest_framework import mixins, generics
class ProductListGeneric(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class CollectionDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    def delete(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it has products.'},
                           status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it has products.'},
                           status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    

def debug_view(request):
    return render(request, 'debug.html', {'name': 'Niloy'})

def basic_queries(request):
    # Get all products
    all_products = Product.objects.all()
    
    # Get single product with error handling
    try:
        single_product = Product.objects.get(pk=1)
    except ObjectDoesNotExist:
        single_product = None
    
    # Filter products
    affordable_products = Product.objects.filter(price__lt=120)
    
    # First product or None
    first_product = Product.objects.filter(price__lt=120).first()
    
    # Check existence
    is_expensive = Product.objects.filter(price__gt=200).exists()
    
    return render(request, 'queries.html', {
        'all_products': list(all_products),
        'single_product': single_product,
        'affordable_products': list(affordable_products),
        'first_product': first_product,
        'is_expensive': is_expensive
    })
    
def complex_queries(request):
    # AND conditions (two ways)
    method1_products = Product.objects.filter(
        inventory__lt=10,
        price__lt=20
    )
    
    method2_products = Product.objects.filter(
        inventory__lt=10
    ).filter(
        price__lt=20
    )
    
    # OR conditions using Q
    discounted_or_low = Product.objects.filter(
        Q(inventory__lt=10) | Q(price__lt=20)
    )
    
    # NOT condition
    not_low_inventory = Product.objects.filter(
        ~Q(inventory__lt=10)
    )
    
    # Compare fields using F
    inventory_equals_price = Product.objects.filter(
        inventory=F('price')
    )
    
    return render(request, 'complex_queries.html', {
        'method1': list(method1_products),
        'method2': list(method2_products),
        'discounted_or_low': list(discounted_or_low),
        'not_low': list(not_low_inventory),
        'inventory_equals_price': list(inventory_equals_price)
    })
    
def query_demo(request):
    # Ordering products
    ordered_products = Product.objects.order_by('title', '-price')[:5]
    
    # Earliest/Latest
    newest_product = Product.objects.latest('last_update')
    oldest_product = Product.objects.earliest('last_update')
    
    # Pagination
    page_2_products = Product.objects.all()[5:10]
    
    # Select specific columns
    product_details = Product.objects\
        .values('title', 'price', 'collection__title')\
        .distinct()
    
    return render(request, 'query_demo.html', {
        'ordered_products': ordered_products,
        'newest_product': newest_product,
        'oldest_product': oldest_product,
        'page_2_products': page_2_products,
        'product_details': product_details
    })
    
def field_selection_demo(request):
    # Using only() - fetches only specified fields
    products_only = Product.objects\
        .only('title', 'price')\
        .all()
    
    # Using defer() - fetches all except specified fields
    products_defer = Product.objects\
        .defer('description', 'last_update')\
        .all()
    
    # Demonstrating additional query issue
    # This will generate extra query because description wasn't fetched
    first_product_desc = products_only.first().description
    
    # Using values() - safer alternative
    products_values = Product.objects\
        .values('title', 'price')
    
    return render(request, 'field_selection.html', {
        'products_only': products_only,
        'products_defer': products_defer,
        'products_values': products_values,
        'first_product_desc': first_product_desc
    })
    
def preload_demo(request):
    # Without select_related (generates N+1 queries)
    products_inefficient = Product.objects.all()
    
    # With select_related for ForeignKey relationships
    products_efficient = Product.objects\
        .select_related('collection')\
        .all()
    
    # Combining select_related and prefetch_related
    products_with_relations = Product.objects\
        .select_related('category')\
        .prefetch_related('promotions')\
        .all()
    
    return render(request, 'preload.html', {
        'products_inefficient': products_inefficient,
        'products_efficient': products_efficient,
        'products_with_relations': products_with_relations
    })
    
def aggregate_demo(request):
    # Basic aggregation
    product_stats = Product.objects.aggregate(
        count=Count('id'),
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    
    # Annotation with proper type casting
    products_with_status = Product.objects.annotate(
        inventory_value=F('price') * F('inventory'),
        is_low_stock=Case(
            When(inventory__lt=10, then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    )
    
    # Collection statistics
    collection_stats = Product.objects.values('collection__title').annotate(
        products_count=Count('id'),
        min_price=Min('price')
    )
    
    return render(request, 'aggregate.html', {
        'stats': product_stats,
        'products_with_status': products_with_status,
        'collection_stats': collection_stats
    })
    

def data_operations(request):
    try:
        with transaction.atomic():
            # Method 1: Update using update()
            Product.objects\
                .filter(inventory__lt=10)\
                .update(price=F('price') * 1.1)

            # Method 2: Update using get() and save()
            product = Product.objects.get(pk=1)
            product.inventory = 100
            product.save()

            # Delete products with zero inventory
            Product.objects\
                .filter(inventory=0)\
                .delete()

            # Get updated products to display
            updated_products = Product.objects\
                .filter(inventory__gt=0)\
                .order_by('price')[:5]

        success = True
        message = "Operations completed successfully"
    except Exception as ex:
        success = False
        message = str(ex)
        updated_products = []

    return render(request, 'data_operations.html', {
        'success': success,
        'message': message,
        'updated_products': updated_products
    })