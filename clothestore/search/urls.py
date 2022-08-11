from django.urls import path

from .views import search_object

app_name = "search"
urlpatterns = [
    path("", search_object, name="search_object")
]
