# Djnago
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# My apps
from clothes.models import PledgeColorSet, Size

# Thist app
from .models import Cart

class CartView(View):

    def post(self, request):
        cart = request.user.cart
        try:
            cart.cartpledge_set.create(
                pledgecolorset = get_object_or_404(
                    PledgeColorSet, 
                    color__name=request.POST.get("color"), 
                    pledge__pk=request.POST.get("pledge"),
                ),
                size=get_object_or_404(
                    Size,
                    name=request.POST.get("size")
                ),
            )
        except ValueError:
            pass
        return redirect(to="cart:cart_path")

    def get(self, request):
        cart = request.user.cart
        return render(
            request=request,
            template_name="cart/cart.html",
            context={
                'total_price': cart.total_price(),
                'products': cart.cartpledge_set.all()
            }
        )

class DeleteProductView(View):
    def post(self, request):
        cart = request.user.cart

        try:
            cart.cartpledge_set.get(id=request.POST.get("id")).delete()
            return redirect(to="cart:cart_path")
        except ObjectDoesNotExist:
            raise Http404()