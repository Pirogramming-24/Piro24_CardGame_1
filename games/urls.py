from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('startPage/<int:pk>/',views.generateGame, name='startPage'),
]