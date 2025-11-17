from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer, Cart
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

def contact(request):
    return render(request, "app/contact.html")


class CategoryView(View):
    
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html",locals())

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfull")
        else:   
            messages.warning(request,"Invalid Input Data")          
        return render(request, 'app/customerregistration.html',locals())
    
class ProfileView(View):  
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            suburb = form.cleaned_data['suburb']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            province = form.cleaned_data['province']
            PostalCode = form.cleaned_data['PostalCode']
            
            reg = Customer(user=user,name=name,suburb=suburb,mobile=mobile,city=city,province=province,PostalCode=PostalCode)
            reg.save()
            messages.success(request,"Congratulations! Profile Saved Successfully")
        else:
            messages.warning(request, "Invalid Input Data")    
        return render(request, 'app/profile.html',locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.suburb = form.cleaned_data['suburb']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.province = form.cleaned_data['province']
            add.PostalCode = form.cleaned_data['PostalCode']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")  
@login_required     
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")
        
@login_required       
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)   
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40    
    return render(request, 'app/addtocart.html',locals())     

class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40    
        return render(request, 'app/checkout.html',locals())
    
def plus_cart(request): 
    if request.method == 'GET': 
        prod_id=request.GET['prod_id'] 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) 
        c.quantity+=1 
        c.save() 
        user = request.user 
        cart = Cart.objects.filter(user=user) 
        amount = 0 
        for p in cart: 
            value = p.quantity * p.product.discounted_price 
            amount = amount + value 
        totalamount = amount + 40
        data={ 
             'quantity':c.quantity,
             'amount':amount, 
             'totalamount':totalamount,
        } 
        return JsonResponse(data)
    

def minus_cart(request): 
    if request.method == 'GET': 
        prod_id=request.GET['prod_id'] 
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) 
        c.quantity-=1 
        c.save() 
        user = request.user 
        cart = Cart.objects.filter(user=user) 
        amount = 0 
        for p in cart: 
            value = p.quantity * p.product.discounted_price 
            amount = amount + value 
        totalamount = amount + 40
        data={ 
             'quantity':c.quantity,
             'amount':amount, 
             'totalamount':totalamount,
        } 
        return JsonResponse(data)
    
def remove_cart(request): 
    if request.method == 'GET': 
        prod_id=request.GET['prod_id'] 
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)) 
        c.delete()
        user = request.user 
        cart = Cart.objects.filter(user=user) 
        amount = 0 
        for p in cart: 
            value = p.quantity * p.product.discounted_price 
            amount = amount + value 
        totalamount = amount + 40
        data={ 
             'amount':amount, 
             'totalamount':totalamount,
        } 
        return JsonResponse(data)
       
    