from django.contrib import admin
from .models import Movie, MovieStatistics

# Register your models here.
admin.site.register(Movie)
admin.site.register(MovieStatistics)
