
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('addtocart/<int:id>/', addtocart, name='addtocart'),
    path('remove_cart/<int:id>/', remove_cart, name='remove_cart'),
    path('decrement_cart/<int:id>/', decrement_cart, name='decrement_cart'),
    path('increment_cart/<int:id>/', increment_cart, name='increment_cart'),
    path('cart_page/<int:id>/', cart_page, name='cart_page'),
    path('payment_gateway/', payment_gateway, name='payment_gateway'),
        path('payment-success/', payment_success, name='payment_success'),
    path('payment-fail/', payment_fail, name='payment_fail'),
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
]