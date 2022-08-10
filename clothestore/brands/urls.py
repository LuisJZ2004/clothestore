from django.urls import path
from .views import AllBrands, ShowBrand

app_name = 'brands'
urlpatterns = [
    path("", AllBrands.as_view(), name="all_brands"),
    path("<slug>/", ShowBrand.as_view(), name="show_brand"),
]
