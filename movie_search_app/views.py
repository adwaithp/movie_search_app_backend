from django.db import ProgrammingError
from rest_framework import generics, viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Movie, UserFavorite
from .serializers import CustomUserSerializer, MovieSerializer, UserFavoriteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout


class UserRegistration(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserLogin(APIView):
    def post(self, request):

        try:
            email = request.data.get('email')
            password = request.data.get('password')

            user = authenticate(request, username=email, password=password)
            if user:
                # Generate a new token or retrieve the existing token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
        except ProgrammingError as e:
            return Response({'message': e})


class UserLogout(APIView):
    def post(self, request):
        # Log the user out
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)


class CustomPagination(PageNumberPagination):
    page_query_param = 'page'  # Specify the query parameter for the page number
    page_size = 15  # Set the number of items per page
    page_size_query_param = 'page_size'  # Specify the query parameter for page size
    max_page_size = 100  # Set the maximum page size

    def get_paginated_response(self, data):
        return Response({
            'current_page': self.page.number,  # Include the current page number in the response
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all().order_by('id')
    serializer_class = MovieSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Movie.objects.all()
        search_query = self.request.query_params.get('keyword')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MovieDetailAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AddFavoriteMovie(APIView):

    def get(self, request, *args, **kwargs):
        movie_id = kwargs.get('pk')
        user = self.request.user
        try:
            user_favorite = UserFavorite.objects.get(user=user, movie_id=movie_id)
            return Response({"is_favorite": True}, status=status.HTTP_200_OK)
        except UserFavorite.DoesNotExist:
            return Response({"is_favorite": False}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            movie_id = kwargs.get('pk')
            movie = Movie.objects.get(id=movie_id)
            UserFavorite.objects.create(user=user,movie=movie)
            return Response({"is_favorite": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({f"Something went wrong {e}"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            movie_id = kwargs.get('pk')
            user_favorite = UserFavorite.objects.get(user=user, movie_id=movie_id)
            user_favorite.delete()
            return Response({"is_favorite": False}, status=status.HTTP_200_OK)
        except UserFavorite.DoesNotExist:
            return Response({"is_favorite": False}, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class FavoriteMovieList(generics.ListAPIView):
    serializer_class = UserFavoriteSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user  # Get the currently authenticated user
        queryset = UserFavorite.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        response_data = []

        for favorite in queryset:
            movie_data = {
                "id": favorite.movie.id,
                "title": favorite.movie.title,
                "overview": favorite.movie.overview,
                "rating": favorite.movie.rating,
                "release_date": favorite.movie.release_date,
            }
            response_data.append(movie_data)

        return Response(response_data)


