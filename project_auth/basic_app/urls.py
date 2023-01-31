from django.urls import path
from . import views as v

app_name = 'basic_app' # template tag

urlpatterns = [
    path("register/", v.register, name="register"),
    path("user_login/", v.user_login, name="user_login"),
]
