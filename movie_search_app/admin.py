from django.contrib import admin
from .models import CustomUser,Movie,UserFavorite
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Movie)
admin.site.register(UserFavorite)