from django.db import ProgrammingError
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Movie
from .serializers import CustomUserSerializer, MovieSerializer
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
            print("Login api called")
            email = request.data.get('email')
            print(email)
            password = request.data.get('password')
            print(password)

            user = authenticate(request, username=email, password=password)
            print(user)
            if CustomUser.objects.filter(email=email, password=password).exists():
                print("User exists")
            else:
                print("Not exists")

            if user:
                # Generate a new token or retrieve the existing token
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
        except ProgrammingError as e:
            print(e)
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
            print(search_query)
            queryset = queryset.filter(title__icontains=search_query)

        return queryset


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MovieDetailAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
