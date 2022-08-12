from django.shortcuts import render, redirect

from .forms import UserRegisterForm

# Create your views here.

def sign_in(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
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