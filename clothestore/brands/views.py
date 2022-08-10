from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Brand

# Create your views here.

class AllBrands(ListView):
    model = Brand
    template_name = "brands/all_brands.html"
    context_object_name = "brands"

    def get_queryset(self):
        return Brand.objects.all()

class ShowBrand(DetailView):
    model = Brand
    template_name = "brands/show_brand.html"

    def get_object(self):
        return get_object_or_404(self.model, slug=self.kwargs['slug'])