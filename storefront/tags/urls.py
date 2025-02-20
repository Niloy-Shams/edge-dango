from django.urls import path
from . import views

urlpatterns = [
    path('generic/', views.generic_relationships_demo, name='generic-demo'),
]