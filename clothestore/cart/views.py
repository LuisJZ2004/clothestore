from django.shortcuts import render
from django.views import View

from .models import Cart

class CartView(View):

    def get(self, request):
        cart = request.user.cart
        return render(
            request=request,
            template_name="cart/cart.html",
            context={
                'total_price': cart.total_price()
            }
        )
