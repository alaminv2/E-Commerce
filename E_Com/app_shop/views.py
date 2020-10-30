from django.shortcuts import render
from app_shop.models import Category, Product
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.


class homeView(ListView):
    model = Product
    template_name = "app_shop/home_page.html"


class productView(DetailView, PermissionRequiredMixin):
    model = Product
    template_name = 'app_shop/product_page.html'
