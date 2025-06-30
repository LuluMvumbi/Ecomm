from django.shortcuts import render
from app.models import *    
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def getProducts(request):

    Products = Product.objects.all()
    print("Products", Products)
    count = 0
    ProductList = []
    for product in Products:
        count += 1
        ProductList.append({
        'tittle': product.tittle,  
        'selling_price': product.selling_price,
        'discounted_price': product.discounted_price,
        'description': product.description
        
    } )
    return JsonResponse(ProductList, safe=False)


