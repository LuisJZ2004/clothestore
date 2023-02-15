from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import sign_in, CustomLoginView

app_name="accounts"
urlpatterns = [
    path("sign_in/", sign_in, name="sign_in"),
    path("login/", CustomLoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
