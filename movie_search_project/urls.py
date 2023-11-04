from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path
from movie_search_app.views import UserRegistration, UserLogin, MovieList, MovieDetailAPIView, UserLogout, \
    AddFavoriteMovie,FavoriteMovieList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('register/', UserRegistration.as_view(), name='user-registration'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('favorites/add/', AddFavoriteMovie.as_view(), name='add-favorite-movie'),
    path('favorites/add/<int:pk>/', AddFavoriteMovie.as_view(), name='add-favorite-movie'),
    path('favorites/', FavoriteMovieList.as_view(), name='user-favorite-list'),
]
