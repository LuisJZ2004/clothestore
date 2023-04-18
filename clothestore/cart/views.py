# Djnago
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# My apps
from clothes.models import PledgeColorSet, Size

# Thist app
from .models import Cart
from .forms import PaymentForm

class CartView(View):
    """
    Shows every product in the cart and can add the through POST method
    """
    def post(self, request):
        """
        Add a product to the cart
        """
        cart = request.user.cart
        try:
            cart.cartpledge_set.create(
                pledgecolorset = get_object_or_404(
                    PledgeColorSet, 
                    color__slug=request.POST.get("color"), 
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
        """
        Shows all the products in the cart andthe total price to pay 
        """
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
        """
        Removes a sended product from the cart
        """
        # I hate with all my strenght to have to use 'POST' method instead of using 'PUT' or 'DELETE' when
        # they are the ones I should use, but in this case, the DELETE method in the html form wasn't working, 
        # so I had to do it like this.
        
        cart = request.user.cart

        try:
            cart.cartpledge_set.get(id=request.POST.get("id")).delete()
            return redirect(to="cart:cart_path")
        except ObjectDoesNotExist:
            raise Http404()

def payment_view(request):
    """
    Shows a payment form (obviously it doesn't take real money) and if the form is valid the cart gets empty,
    else it returns an error message with the form again.
    """

    if request.user.cart.products.all():
        form = PaymentForm()
        
        if request.method == 'POST':
            form = PaymentForm(request.POST)
            if form.is_valid():
                try:
                    card_number = int(request.POST["card_number"])
                    cvv = int(request.POST["cvv"])
                except:
                    return render(request, 'cart/payment.html', 
                        context= {
                            "number_error": True,
                            "form": PaymentForm(),
                        }
                    )
                request.user.cart.succesful_purchase()
                request.user.cart.products.clear()

                return render(request, 'cart/payment.html', {"confirm_message": True})
            else:
                return render(
                    request, 
                    'cart/payment.html',
                    context={
                        'form': PaymentForm(),
                        'errors': form.errors,
                    }
                )
        return render(
            request, 
            'cart/payment.html', 
            {'form': form}
        )
    else:
        return redirect(to="cart:cart_path")