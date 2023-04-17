from django.urls import path

from .views import search_object_view

app_name = "search"
urlpatterns = [
    path("", search_object_view, name="search_object")
]
