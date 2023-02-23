from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

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
            print(dict(form.errors))
            context = {
                'form': form,
                'errors': dict(form.errors),
            }
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

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        # In the default LoginView it doesn't return the errors if any, so I send them if the form is not valid
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors))