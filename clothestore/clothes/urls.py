from django.urls import path

from .views import ClothingTypeView, clothes_by_gender, ShowPledge

app_name = 'clothes'
urlpatterns = [
    path("<str:gender>/", ClothingTypeView.as_view(), name="clothes_by_gender"),
    path("pledges/<pk>/", ShowPledge.as_view(), name="show_pledge")
]
