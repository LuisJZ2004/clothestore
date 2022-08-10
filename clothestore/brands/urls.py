from django.urls import path
from .views import AllBrands

app_name = 'brands'
urlpatterns = [
    path("", AllBrands.as_view(), name="all_brands"),
]
