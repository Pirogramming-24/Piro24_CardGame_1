from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('<int:pk>/counter/', views.counter_attack, name='counter_attack'),
    path('<int:pk>/', views.detail, name='detail'),
]