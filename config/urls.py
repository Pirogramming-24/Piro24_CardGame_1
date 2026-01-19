"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated:
        return HttpResponse(f"<h1>{request.user.username}님, 로그인 성공!</h1><p>이제 카드 게임을 시작해볼까요?</p>")
    else:
        return HttpResponse("로그인이 필요합니다.")
# from .views import ranking

urlpatterns = [
    path('admin/', admin.site.urls),
    path('games/',include('games.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/',include('accounts.urls')),
    path('',home),
]
