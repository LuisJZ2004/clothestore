from django.shortcuts import render
from django.views.generic import ListView
from .models import ClothingType, Pledge

# Create your views here.

def clothes_by_gender(request, gender):
    clothes = Pledge.objects.filter(gender__in=gender)
    typeclothing = ClothingType.objects.filter(gender__in=gender)
    filter = request.GET.get("filter")
    order = request.GET.get("order")

    orders = {
        "pub-date": "-pub_date",
        "A-Z": "name",
        "Z-A": "-name",
    }

    if filter or order:
        if order and filter:
            clothes = Pledge.objects.filter(gender__in=gender, clothing_type__slug = filter).order_by(orders[order])
        elif order:
            clothes = clothes.order_by(orders[order])
        elif filter:
            clothes = Pledge.objects.filter(gender__in=gender, clothing_type__slug = filter)
        

    context = {
        'gender': gender,
        'pledges': clothes,
        'type_clothing': typeclothing,
        'orders': orders,

        'filter': filter,
        'order': order,
    }

    return render(
        request=request,
        context=context,
        template_name="clothes/clothes_by_gender.html",
    )