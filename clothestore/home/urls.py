from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import Home

app_name="home"
urlpatterns = [
    path("", Home.as_view(), name="home_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
