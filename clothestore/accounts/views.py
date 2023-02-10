from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# My apps
from cart.models import Cart

# This app
from .forms import UserRegisterForm

# Create your views here.

def sign_in(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            Cart.objects.create(user=User.objects.get(username=request.POST["username"]))
            return redirect(to="accounts:login")
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(
        request=request,
        template_name="accounts/sign_in.html",
        context=context
    )