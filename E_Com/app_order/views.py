from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# Models
from app_shop.models import Product
from .models import Cart, Order
# Messages
from django.contrib import messages

# Create your views here.


@login_required
def addToCart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    print('Item =>')
    print(item)
    item_in_cart = Cart.objects.get_or_create(
        user=request.user, item=item, purchased=False)
    # print('Item in Cart =>')
    # print(item_in_cart)
    # print(item_in_cart[0])
    order_query = Order.objects.filter(user=request.user, ordered=False)
    # print('Order Query Set =>')
    # print(order_query)
    if order_query.exists():
        order_list = order_query[0]
        if order_list.orderitems.filter(item=item).exists():
            item_in_cart[0].quantity += 1
            item_in_cart[0].save()
            messages.info(
                request, 'Item quantity has changed successfully......!')
            return redirect('app_shop:home')
        else:
            order_list.orderitems.add(item_in_cart[0])
            messages.info(
                request, 'This item is successfully added to your Cart')

    else:
        new_order = Order(user=request.user)
        new_order.save()
        new_order.orderitems.add(item_in_cart[0])
        messages.info(request, 'This item is successfully added to your Cart')
        return redirect('app_shop:home')

    return redirect('app_shop:home')


@login_required
def cartView(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    all_orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and all_orders.exists():
        orders = all_orders[0]
        return render(request, 'app_order/cart_page.html', context={'carts': carts, 'orders': orders})
    else:
        messages.warning(request, 'You have no items in Cart.......!!!')
        return redirect('app_shop:home')


@login_required
def increaseQuantity(request, pk):
    cart_obj = Cart.objects.get(pk=pk)
    cart_obj.quantity += 1
    cart_obj.save()
    messages.info(request, 'Quantity increased.........')
    return redirect('app_order:cart')


@login_required
def decreaseQuantity(request, pk):
    cart_obj = Cart.objects.get(pk=pk)
    if cart_obj.quantity > 1:
        cart_obj.quantity -= 1
        cart_obj.save()
        messages.info(request, 'Quantity decreased.........')
    else:
        messages.warning(request, "Quantity can not be '0'")
    return redirect('app_order:cart')


@login_required
def removeFromCart(request, pk):
    cart_obj = Cart.objects.get(pk=pk)
    print(f'cart_obj = {cart_obj}')
    cart_obj.delete()
    messages.success(request, 'Item removed successfully......')
    return redirect('app_order:cart')
