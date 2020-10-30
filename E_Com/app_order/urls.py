from django.urls import path
from . import views

app_name = 'app_order'

urlpatterns = [
    path('add/<pk>/', views.addToCart, name="add_to_cart"),
    path('cart/', views.cartView, name="cart"),
    path('increase/<pk>/', views.increaseQuantity, name="increase_quantity"),
    path('decrease/<pk>/', views.decreaseQuantity, name="decrease_quantity"),
    path('remove/<pk>/', views.removeFromCart, name="remove"),
]
