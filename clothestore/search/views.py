from django.shortcuts import render, redirect
from django.db.models import Q

from clothes.models import Pledge
from brands.models import Brand

# Create your views here.

def search_object(request):
    search = request.GET["search-bar"]

    if search:
        pledges = Pledge.objects.filter(
            Q(name__icontains = search) |
            Q(description__icontains = search)
        )
        brands = Brand.objects.filter(
            name__icontains = search
        )
    else:
        return redirect(to="home:home_page")

    context = {
        'pledges': pledges, 
    }

    return render(
        request=request,
        template_name="search/search.html",
        context=context,
    )