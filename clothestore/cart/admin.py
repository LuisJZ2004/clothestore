from django.contrib import admin
from .models import Cart, CartPledge, SuccesfulPurchase
# Register your models here.

admin.site.register(
    [
        Cart,
        CartPledge,
        SuccesfulPurchase,
    ]
)
