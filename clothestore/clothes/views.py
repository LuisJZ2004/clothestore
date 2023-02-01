from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.views.generic import DetailView, ListView
from .models import ClothingType, Pledge

# Create your views here.

class ClothingTypeView(ListView):
    model=ClothingType
    template_name="clothes/clothing_type.html"
    context_object_name="clothing_types"

    def get_queryset(self):
        query_set = self.model.objects.filter(gender=self.kwargs["gender"])
        if query_set:
            return query_set
        
        raise Http404()
            
    
def clothes_list_view(request, gender, slug):
    pledges = Pledge.objects.filter(clothing_type__slug=slug, gender=gender)
    
    return render(
        request=request,
        template_name="clothes/clothes_list.html",
        context={
            "pledges": pledges
        }
    )

def clothes_by_gender(request, gender):
    """
    Shows all the clothes belonging to a gender.
    It can do filters by the type of clothing and odering by name or publish date
     
    Obligatory parameters:
    - gender: the gender of the clothes.

    Optional parameters:
    - filter: the clothing type to filter.
    - order: the order in which the products will be shown 
    """
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

class ShowPledge(DetailView):
    model = Pledge
    template_name = "clothes/pledge.html"

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))