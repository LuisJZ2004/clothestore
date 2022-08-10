from django.urls import path

from .views import clothes_by_gender, ShowPledge

app_name = 'clothes'
urlpatterns = [
    path("<str:gender>/", clothes_by_gender, name="clothes_by_gender"),
    path("pledges/<pk>/", ShowPledge.as_view(), name="show_pledge")
]
