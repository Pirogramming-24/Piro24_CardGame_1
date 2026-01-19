from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path("", views.main, name="main"),
    path('startPage/',views.generateGame, name='startPage'),
    path('gameList/',views.gameList,name='gameList'),
    path('<int:pk>/counter/', views.counter_attack, name='counter_attack'),
    path('<int:pk>/', views.detail, name='detail'),
    path('ranking',views.ranking,name='ranking'),
]