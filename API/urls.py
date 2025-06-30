from django.urls import path, include
from . import views



urlpatterns = [
    path('products/', views.getProducts, name='getproducts'),  
]