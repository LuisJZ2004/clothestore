# Django
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.views.generic import DetailView, ListView

# This app
from .models import ClothingType, Pledge, PledgeColorSet

# My apps
from extra_logic.clothes.functions import make_pagination, get_pagination_numbers, remove_duplicates
from extra_logic.clothes.classes import Filter, QuantityOfAField

class ClothingTypeView(ListView):
    """
    Shows all the available clothing types for a respective gender
    """
    model=ClothingType
    template_name="clothes/clothing_type.html"
    context_object_name="clothing_types"

    def get_queryset(self):
        query_set = self.model.objects.filter(gender=self.kwargs["gender"])
        if query_set:
            return query_set
        
        raise Http404()
            
    
def clothes_list_view(request, gender, slug):
    """
    List of the products belonging to a clothing type. They can be filtered with extra algorythms I made
    """
    # First we get the pledgecolorsets ordered by publish date
    sets = PledgeColorSet.objects.filter(pledge__clothing_type__slug=slug, pledge__gender=gender).order_by("-pub_date")

    # Orders we'll send in the end to the template
    orders = {
        "pub date (old to lastest)": "pub_date",
        "pub date (lastest to old)": "-pub_date",
        "A-Z": "pledge__name",
        "Z-A": "-pledge__name",
        "price (higher to lower)": "-price",
        "price (lower to higher)": "price"
    }
    page_numbers = range(1, get_pagination_numbers(sets, 5)+1)
    page = None

    selected_color = None
    selected_size = None
    selected_order = None

    query_len = None

    # We can filter the queryset through a html form with 'POST' method
    if request.method == "POST":
        # We get the color, size and order, if any of them wasn't sended, just None
        selected_color = request.POST.get("color")
        selected_size = request.POST.get("size")
        selected_order = request.POST.get("order")

        # Just in case a string is sended instead a number in the pages 
        try:
            if request.POST.get("page") != None:
                page = int(request.POST.get("page"))
        except ValueError:
            return redirect(to="clothes:pledge_list_path", gender=gender, slug=slug)

        # We make the fields with their respective query string
        filters = {
            "fields": {
                "sizes__name": selected_size,
                "color__name": selected_color,
            },
            "order": request.POST.get("order"),
        }
        # We filter the queryset with the class Filter
        filtering = Filter()
        sets = filtering.get_queryset_filtered(sets.distinct(), filters["fields"], order=filters["order"])

    query_len = len(sets)
    # We get the quantity of pages there are for this queryset
    page_numbers = range(1, get_pagination_numbers(sets, 5)+1)
    # We get the quantity of colors and sizes there are in each product of the queryset
    quantities = QuantityOfAField().get_quantity_of_each_field(sets, selected_color, selected_size)
    
    # Paginate 5 by 5
    if page and page != 0:
        aux = sets
        sets = make_pagination(sets, page, 5)
        if not sets:
            sets = make_pagination(aux, 1, 5)
            page_numbers = range(1, get_pagination_numbers(aux, 5)+1)
    else:
        sets = make_pagination(sets, 1, 5)

    return render(
        request=request,
        template_name="clothes/clothes_list.html",
        context={
            "sets": sets,
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

# This was the first view for pledges
# def clothes_by_gender(request, gender):
#     """
#     Shows all the clothes belonging to a gender.
#     It can do filters by the type of clothing and odering by name or publish date
     
#     Obligatory parameters:
#     - gender: the gender of the clothes.

#     Optional parameters:
#     - filter: the clothing type to filter.
#     - order: the order in which the products will be shown 
#     """
#     clothes = Pledge.objects.filter(gender__in=gender)
#     typeclothing = ClothingType.objects.filter(gender__in=gender)
#     filter = request.GET.get("filter")
#     order = request.GET.get("order")

#     orders = {
#         "pub-date": "-pub_date",
#         "A-Z": "name",
#         "Z-A": "-name",
#     }

#     if filter or order:
#         if order and filter:
#             clothes = Pledge.objects.filter(gender__in=gender, clothing_type__slug = filter).order_by(orders[order])
#         elif order:
#             clothes = clothes.order_by(orders[order])
#         elif filter:
#             clothes = Pledge.objects.filter(gender__in=gender, clothing_type__slug = filter)
        

#     context = {
#         'gender': gender,
#         'sets': clothes,
#         'type_clothing': typeclothing,
#         'orders': orders,

#         'filter': filter,
#         'order': order,
#     }

#     return render(
#         request=request,
#         context=context,
#         template_name="clothes/clothes_by_gender.html",
#     )

class ShowPledge(DetailView):
    """
    Shows a pledgecolorset with all its details
    """
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
            pledgecolorset_selected = get_object_or_404(PledgeColorSet, pledge=self.get_object(), color__slug=self.color)

        return {
            self.context_object_name: self.get_object(),
            "pledgecolorsets": self.get_object().pledgecolorset_set.all(),
            "pledgecolorset_selected": pledgecolorset_selected
        }