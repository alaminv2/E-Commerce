from django.urls import path
from . import views

app_name = 'app_payment'

urlpatterns = [
    path('checkout/', views.checkOutView, name="checkout"),
    path('pay/', views.paymentView, name="payment"),
    path('status/', views.completePayment, name="status"),
    path('purchased/<val_id>/<tran_id>/',
         views.purchasedView, name="purchased"),
    path('orders/', views.paidOrders, name="orders"),
]
