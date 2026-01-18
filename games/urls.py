from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path("", views.main, name="main"),
]