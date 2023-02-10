# Django
from django.urls import path
from django.contrib.auth.decorators import login_required

# This app
from .views import CartView

app_name="cart"
urlpatterns = [
    path("", login_required(CartView.as_view()), name="cart_path"),
]
