# Django
from django.urls import path
from django.contrib.auth.decorators import login_required

# This app
from .views import CartView, DeleteProductView

app_name="cart"
urlpatterns = [
    path("", login_required(CartView.as_view()), name="cart_path"),
    path("delete/", login_required(DeleteProductView.as_view()), name="delete_product_path"),
]
