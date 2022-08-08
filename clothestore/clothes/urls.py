from django.urls import path

from .views import clothes_by_gender

app_name = 'clothes'
urlpatterns = [
    path("<str:gender>/", clothes_by_gender, name="clothes_by_gender")
]
