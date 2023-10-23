"""
URL configuration for movie_search_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from movie_search_app.views import UserRegistration, UserLogin, MovieList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('movies/', MovieList.as_view(), name='movie-list'),
]