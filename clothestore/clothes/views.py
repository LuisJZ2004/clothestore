from django.shortcuts import render
from django.views.generic import ListView
from .models import ClothingType, Pledge

# Create your views here.

def clothes_by_gender(request, gender):
    clothes = Pledge.objects.filter(gender__in=gender)

    context = {
        'pledges': clothes
    }

    return render(
        request=request,
        context=context,
        template_name="clothes/clothes_by_gender.html",
    )