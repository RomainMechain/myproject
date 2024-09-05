from django.urls import path

from . import views

urlpatterns = [
    path("home/<name>", views.index, name="index"),
    path("home/", views.home, name="home")
]