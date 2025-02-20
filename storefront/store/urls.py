from django.urls import path
from . import views

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
]
