import os

import requests
from django.core.validators import MinValueValidator, MinLengthValidator
from django.contrib.auth.models import User
from django.db import models
from dotenv import load_dotenv

load_dotenv()


class MovieStatistics(models.Model):
    vote_average = models.DecimalField(max_digits=5, decimal_places=2,
                                       validators=[MinValueValidator(1)])
    vote_count = models.IntegerField()
    popularity = models.DecimalField(max_digits=20, decimal_places=10)


# Create your models here.
class Movie(models.Model):
    tmdb_id = models.CharField(max_length=255)
    original_title = models.CharField(max_length=1000)
    overview = models.TextField()
    release_date = models.DateField()
    cast = models.CharField(max_length=1000)
    genres = models.CharField(max_length=1000)
    director = models.CharField(max_length=1000)
    keywords = models.TextField(validators=[MinLengthValidator(10)])
    statistics = models.OneToOneField(MovieStatistics, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.original_title}"

    @staticmethod
    def movie_with_tile_exist(title: str):
        found_count = Movie.objects.filter(original_title=title).count()
        return found_count > 0

    @staticmethod
    def create_from_form(form_data):
        initial_statistics = MovieStatistics.objects.create(vote_average=0, vote_count=0, popularity=0)

        Movie.objects.create(
            tmdb_id=form_data['tmdb_id'],
            original_title=form_data['title'],
            overview=form_data['overview'],
            release_date=form_data['release_date'],
            cast=form_data['cast'],
            genres=form_data['genres'],
            director=form_data['director'],
            keywords=form_data['keywords'],
            statistics=initial_statistics
        )

    def poster_url(self):
        if not self.tmdb_id:
            return None

        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{self.tmdb_id}?api_key={os.environ.get("TMDB_APIKEY")}'
            f'&language=en-US')
        data = response.json()

        if response.status_code == 200 and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

        return ''

    def backdrop_image(self):
        if not self.tmdb_id:
            return None
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{self.tmdb_id}?api_key={os.environ.get("TMDB_APIKEY")}')
        data = response.json()

        if response.status_code == 200 and data['backdrop_path']:
            return "https://image.tmdb.org/t/p/w1920_and_h800_multi_faces/" + data['backdrop_path']

        return ''


class MovieCollection(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateField()
    update_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)

    @staticmethod
    def collection_exist(collection_name):
        return MovieCollection.objects.filter(name__contains=collection_name).count() > 0
