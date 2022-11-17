from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("index", views.store, name="index"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.UpdateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
]
