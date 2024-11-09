from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from Accounts.models import profile 
from django.db.models import Q
from Product.models import *
from django.http import HttpResponse
from sslcommerz_lib import SSLCOMMERZ
import random

# Create your views here.

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'home.html', {'products': products, 'categories': categories, 'cart_items_count': cart_items_count})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(cate=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})



def addtocart(request, id):
    user = request.user
    prod = get_object_or_404(Product, id=id)
    
    if user.is_authenticated:
        cartItem = Cart.objects.filter(user=user, prod=prod).first()
        
        if cartItem:
            cartItem.quantity += 1
            cartItem.save()
        else:
            cartItem = Cart.objects.create(user=user, prod=prod, quantity=1)
    
    return redirect('/')

def remove_cart(request, id):
    prod=Product.objects.get(id=id)
    cart_item=Cart.objects.get(user=request.user, prod=prod)
    cart_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def decrement_cart(request, id):
    prod = Product.objects.get(id=id)
    cart_item = Cart.objects.get(user=request.user, prod=prod)
    if cart_item == 1:
        cart_item.delete()
    else:
        cart_item.quantity-=1
        cart_item.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def increment_cart(request, id):
    prod = Product.objects.get(id=id)
    cart_item = Cart.objects.get(user=request.user, prod=prod)
    if cart_item:
        cart_item.quantity+=1
        cart_item.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def cart_page(request, id):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    for item in cart_items:
        item.total_price = item.prod.price * item.quantity 

    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})


def payment_gateway(request): 
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    q = 0
    for item in cart_items:
        item.total_price = item.prod.price * item.quantity
        q += item.quantity 

    total_price = sum(item.total_price for item in cart_items)
    settings = {
        'store_id': 'swing672ef3b97d1c5',
        'store_pass': 'swing672ef3b97d1c5@ssl',
        'issandbox': True
    }
    sslcz = SSLCOMMERZ(settings)
    
    post_body = {
    'total_amount': total_price,
    'currency': "BDT",
    'tran_id': "12345",
    'success_url': request.build_absolute_uri('/products/payment-success/'),
    'fail_url': request.build_absolute_uri('/products/payment-fail/'),
    'cancel_url': request.build_absolute_uri('/products/payment-cancel/'),
    'emi_option': 0,
    'cus_name': user.username,
    'cus_email': user.email,
    'cus_phone': "01700000000",
    'cus_add1': "customer address",
    'cus_city': "Dhaka",
    'cus_country': "Bangladesh",
    'shipping_method': "NO",
    'multi_card_name': "",
    'num_of_item': q,
    'product_name': "Test",
    'product_category': "Test Category",
    'product_profile': "general"
    }
    

    response = sslcz.createSession(post_body)
    return redirect(response['GatewayPageURL'])

def payment_success(request):
    return HttpResponse("Payment was successful! Thank you for your purchase.")

def payment_fail(request):
    return HttpResponse("Payment failed. Please try again.")

def payment_cancel(request):
    return HttpResponse("Payment was canceled. You can try again if you wish.")







