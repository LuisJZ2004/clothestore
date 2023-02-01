from django.urls import path

from .views import ClothingTypeView, clothes_by_gender, ShowPledge, clothes_list_view

app_name = 'clothes'
urlpatterns = [
    path("<str:gender>/", ClothingTypeView.as_view(), name="clothes_by_gender"),
    path("<gender>/<slug>/", clothes_list_view, name="pledge_list_path"),
    path("pledges/<pk>/", ShowPledge.as_view(), name="show_pledge")
]
