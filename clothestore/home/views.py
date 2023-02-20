# Django
from django.shortcuts import render
from django.views.generic import TemplateView

# This app
from .models import HomeSet

class Home(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = {
            "home_sets": HomeSet.objects.all().order_by("-pub_date")
        } 
        return context
    