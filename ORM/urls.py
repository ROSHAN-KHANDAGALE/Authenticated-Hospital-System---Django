from django.urls import path
from . import views

urlpatterns = [
    path("", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("register/", views.Register.as_view(), name="register"),
    path("index/", views.Index.as_view(), name="index"),
    path("forgot/", views.Forgot.as_view(), name="forgot"),
    path("reset/<uuid>", views.Reset.as_view(), name="reset"),
]
