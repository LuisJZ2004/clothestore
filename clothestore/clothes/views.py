# Django
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.views.generic import DetailView, ListView

# This app
from .models import ClothingType, Pledge, PledgeColorSet

# My apps
from extra_logic.clothes.functions import make_pagination, get_pagination_numbers
from extra_logic.clothes.classes import Filter, QuantityOfAField

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

    orders = {
        "pub date": "-pub_date",
        "A-Z": "name",
        "Z-A": "-name",
        "price (higher to lower)": "-pledgecolorset__price",
        "price (lower to higher)": "pledgecolorset__price"
    }
    page_numbers = range(1, get_pagination_numbers(pledges, 5)+1)
    page = None

    selected_color = None
    selected_size = None
    selected_order = None

    query_len = None
    if request.method == "POST":
        selected_color = request.POST.get("color")
        selected_size = request.POST.get("size")
        selected_order = request.POST.get("order")
        # print(selected_order)
        try:
            if request.POST.get("page") != None:
                page = int(request.POST.get("page"))
        except ValueError:
            return redirect(to="clothes:pledge_list_path", gender=gender, slug=slug)

        filters = {
            "fields": {
                "pledgecolorset__sizes__name": selected_size,
                "pledgecolorset__color__name": selected_color,
            },
            "order": request.POST.get("order"),
        }
        filtering = Filter()
        pledges = filtering.get_queryset_filtered(pledges.distinct(), filters["fields"], order=filters["order"])
        query_len = len(pledges)

    quantities = QuantityOfAField().get_quantity_of_each_field(pledges, selected_color, selected_size)
    
    if page and page != 0:
        pledges = make_pagination(pledges, page, 5)
    else:
        pledges = make_pagination(pledges, 1, 5)

    return render(
        request=request,
        template_name="clothes/clothes_list.html",
        context={
            "pledges": pledges,
            "gender": gender,
            "clothing_type_slug": slug,
            "colors": quantities["colors"],
            "sizes": quantities["sizes"],
            
            "selected_color": selected_color,
            "selected_size": selected_size,
            "selected_order": selected_order,

            "orders": orders,

            "query_len": query_len,

            "page": page,
            "page_numbers": page_numbers,
        }
    )

def get_form_checkboxes(request, gender, slug):
    print(request.GET)

    return redirect(to=request.path, gender=gender, slug=slug)

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
    context_object_name = "pledge"

    def dispatch(self, request, *args, **kwargs):

        self.color = request.GET.get("color")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        pledgecolorset_selected = None
        if self.color:
            pledgecolorset_selected = get_object_or_404(PledgeColorSet, pledge=self.get_object(), color__name=self.color)

        return {
            self.context_object_name: self.get_object(),
            "pledgecolorsets": self.get_object().pledgecolorset_set.all(),
            "pledgecolorset_selected": pledgecolorset_selected
        }