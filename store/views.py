from django.shortcuts import render
from django.http import JsonResponse
import datetime
import json
from django.views.decorators.csrf import csrf_exempt

from .models import *


def store(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        shipping = str(order.shipping).lower()
    else:
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        customer = {}
        cartItems = order["get_cart_items"]
        shipping = False

    context = {
        "customer": customer,
        "products": products,
        "order": order,
        "cartItems": cartItems,
        "shipping": shipping,
    }
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        shipping = str(order.shipping).lower()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]
        shipping = False

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": shipping,
    }
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        shipping = str(order.shipping).lower()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]
        shipping = False

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": shipping,
    }
    return render(request, "store/checkout.html", context)


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item Updated", safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        print("total: ", total)
        print("total db: ", order.get_cart_total)

        if round(total, 2) == round(float(order.get_cart_total), 2):
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"],
                country=data["shipping"]["country"],
            )

    else:
        print("user is not logged in")
    return JsonResponse("Payment Submited", safe=False)
