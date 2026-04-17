from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('cart.html/',views.cart,name='cart'),
    path('checkout.html/',views.checkout,name='checkout')
]
