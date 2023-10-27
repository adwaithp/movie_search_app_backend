from django.contrib import admin
from django.urls import path

from movie_search_app.views import UserRegistration, UserLogin, MovieList, MovieDetailAPIView, UserLogout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('logout/', UserLogout.as_view(), name='logout'),
]
