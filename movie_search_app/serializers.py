# serializers.py
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import CustomUser,Movie

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        user = CustomUser.objects.create(**validated_data)
        return user




class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'overview', 'rating', 'release_date']
