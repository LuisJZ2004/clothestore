from django.shortcuts import render
from django.views.generic import ListView
from .models import ClothingType, Pledge

# Create your views here.

def clothes_by_gender(request, gender):
    clothes = Pledge.objects.filter(gender__in=gender)
    typeclothing = ClothingType.objects.filter(gender__in=gender)
    filter = request.GET.get("filter")

    if filter:
        clothes = Pledge.objects.filter(gender__in=gender, clothing_type__slug = filter)

    context = {
        'gender': gender,
        'pledges': clothes,
        'type_clothing': typeclothing
    }

    return render(
        request=request,
        context=context,
        template_name="clothes/clothes_by_gender.html",
    )