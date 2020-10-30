from django.urls import path
from . import views

app_name = 'app_shop'

urlpatterns = [
    path('', views.homeView.as_view(), name="home"),
    path('product/<pk>/', views.productView.as_view(), name="product"),
]
