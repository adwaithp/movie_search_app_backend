from django.contrib import admin
from .models import CustomUser,Movie
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Movie)