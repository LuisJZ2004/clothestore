from django.shortcuts import render
from django.views.generic import ListView

from .models import Brand

# Create your views here.

class AllBrands(ListView):
    model = Brand
    template_name = "brands/all_brands.html"
    context_object_name = "brands"

    def get_queryset(self):
        return Brand.objects.all()