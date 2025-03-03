from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)

urlpatterns = [
    path('products/', views.product_list),
    path('debug/', views.debug_view),
    path('queries/', views.basic_queries, name='basic-queries'),
    path('complex-queries/', views.complex_queries, name='complex-queries'),
    path('query-demo/', views.query_demo, name='query-demo'),
    path('field-selection/', views.field_selection_demo, name='field-selection'),
    path('preload/', views.preload_demo, name='preload-demo'),
    path('aggregate/', views.aggregate_demo, name='aggregate-demo'),
    path('data-operations/', views.data_operations, name='data-operations'),
    path('products-drf/', views.product_list_drf),
    path('products-drf/<int:pk>/', views.product_detail_drf),
    path('collections/', views.collection_list),
    path('collections/<int:pk>/', views.collection_detail),
    path('collections-class/', views.CollectionListClass.as_view()),
    path('products-generic/', views.ProductListGeneric.as_view()),
    path('products-generic/<int:pk>/', views.ProductDetailGeneric.as_view()),
    path('collection-generic/<int:pk>/', views.CollectionDetailGeneric.as_view()),
    path('viewset/', include(router.urls)),
]
