from django.shortcuts import render, redirect, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Models and Forms
from .forms import BillingForm
from .models import BillingAddress
from app_order.models import Order, Cart

# For Payment
import requests
import socket
from decimal import Decimal
from sslcommerz_python.payment import SSLCSession
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@login_required
def checkOutView(request):
    diction = {}
    bill_obj = BillingAddress.objects.get_or_create(user=request.user)
    bill_obj = bill_obj[0]
    form = BillingForm(instance=bill_obj)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=bill_obj)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=bill_obj)
            messages.success(
                request, 'Billing address successfully saved....!')

    orders = Order.objects.filter(user=request.user, ordered=False)
    # print(f'Orders\n{orders}')
    order_list = orders[0].orderitems.all()
    # print(f'Order List\n {order_list}')

    total_amount = orders[0].order_total()
    # print(f'Total Amount = {total_amount}')
    diction.update({'form': form})
    diction.update({'order_list': order_list})
    diction.update({'total_amount': total_amount})
    diction.update({'bill_obj': bill_obj})

    return render(request, 'app_payment/checkout_page.html', context=diction)


@login_required
def paymentView(request):
    bill_obj = BillingAddress.objects.get_or_create(user=request.user)
    bill_obj = bill_obj[0]
    if not bill_obj.is_fully_filled():
        messages.warning(
            request, 'Please make sure Shipping Address is filled up')
        return redirect('app_payment:checkout')
    if not request.user.profile.is_fully_filled():
        messages.warning(
            request, 'Please make sure Profile details is filled up')
        return redirect('app_login:profile')

    Store_Id = 'alami5f6e0c81e4c39'
    API_key = 'alami5f6e0c81e4c39@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True,
                            sslc_store_id=Store_Id, sslc_store_pass=API_key)

    status_url = request.build_absolute_uri(reverse('app_payment:status'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)

    order = Order.objects.filter(user=request.user, ordered=False)
    totalAmount = order[0].order_total()
    productName = order[0].orderitems.all()
    numOfItem = order[0].orderitems.count()
    # print(f' {totalAmount}   {productName}    {numOfItem} ')
    mypayment.set_product_integration(total_amount=Decimal(totalAmount), currency='BDT', product_category='Mixed',
                                      product_name=productName, num_of_item=numOfItem, shipping_method='Curier', product_profile='None')

    current_user = request.user
    Name = current_user.profile.full_name
    Email = current_user.email
    Address = current_user.profile.address_1
    City = current_user.profile.city
    Postcode = current_user.profile.zipcode
    Country = current_user.profile.country
    Phone = current_user.profile.phone
    # print(Name)
    # print(Email)
    # print(Address)
    # print(City)
    # print(Postcode)
    # print(Country)
    # print(Phone)
    mypayment.set_customer_info(name=Name, email=Email, address1=Address,
                                address2=Address, city=City, postcode=Postcode, country=Country, phone=Phone)

    mypayment.set_shipping_info(shipping_to=Name, address=bill_obj.address,
                                city=bill_obj.city, postcode=bill_obj.zipcode, country=bill_obj.country)

    response_data = mypayment.init_payment()
    # print(response_data)
    # messages.success(request, 'Payment Successful')
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def completePayment(request):
    if request.method == 'POST' or request.method == 'post':
        if request.method == 'POST':
            payment_data = request.POST
        elif request.method == 'post':
            payment_data = request.post

        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']
            messages.success(request, 'Payment completed successfully.......')

            risk_level = payment_data['risk_level']
            if risk_level == '1':
                messages.warning(
                    request, 'Be carefull. There was a risk......')
            return HttpResponseRedirect(reverse('app_payment:purchased', kwargs={'val_id': val_id, 'tran_id': tran_id}))

        elif status == 'FAILED':
            messages.warning(
                request, 'Sorry... Payment cannot be completed.......')

    return render(request, 'app_payment/status_page.html', context={})


@login_required
def purchasedView(request, val_id, tran_id):
    order = Order.objects.filter(user=request.user, ordered=False)
    order = order[0]
    print(f'Order.ordered = {order.ordered}')
    order.ordered = True
    order.order_id = val_id
    order.payment_id = tran_id
    order.save()
    print(f'Order is => {order}')
    print('----------For Cart------------')
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        print(f'{item.item.name}  {item.purchased}')
        item.purchased = True
        item.save()

    return redirect(reverse('app_shop:home'))


@login_required
def paidOrders(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        print(orders)
    except:
        messages.warning(request, 'No Recent Orders Here...')
    return render(request, 'app_payment/paid_order_page.html', context={'orders': orders})
