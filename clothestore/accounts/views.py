from django.shortcuts import render

# Create your views here.

def sign_in(request):
    context = {}
    return render(
        request=request,
        template_name=None,
        context=context
    )