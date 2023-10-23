from django.db import ProgrammingError
from rest_framework import generics
from .models import CustomUser, Movie
from .serializers import CustomUserSerializer, MovieSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


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
            if CustomUser.objects.filter(email=email,password=password).exists():
                print("User exists")
            else:
                print("Not exists")

            if user:
                # Generate a new token or retrieve the existing token
                token, created = Token.objects.get_or_create(user=user)

                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
        except ProgrammingError  as e:
            print(e)
            return Response({'message': e})


class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()

        # Check if a search query parameter is provided
        search_query = self.request.query_params.get('keyword')
        if search_query:
            # Filter movies based on the search query
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

