from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import sign_in

app_name="accounts"
urlpatterns = [
    path("sign_in/", sign_in, name="sign_in"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
