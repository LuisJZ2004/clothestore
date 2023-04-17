from django.shortcuts import render, redirect
from django.db.models import Q

from clothes.models import PledgeColorSet
from brands.models import Brand

# Create your views here.

def search_object_view(request):
    search = request.GET.get("search-bar")

    if search:
        pledges = PledgeColorSet.objects.filter(
            Q(pledge__name__icontains = search) |
            Q(color__name__icontains = search) |
            Q(pledge__brand__name__icontains = search) 
        ).distinct()
    else:
        return redirect(to="home:home_page")

    context = {
        'search': search,
        'sets': pledges,
    }

    return render(
        request=request,
        template_name="search/search.html",
        context=context,
    )