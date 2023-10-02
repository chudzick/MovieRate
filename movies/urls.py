from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_movies, name='all_movies'),
    path('<int:id>', views.find_by_tmdb_id, name='movie'),
    path('add', views.add_movie, name='add_movie'),
    path('collections', views.movie_collections, name='all_collections'),
    path('collections/<int:id>', views.collection_details, name='collection'),
    path('collections/add/movie/<int:movie_id>', views.add_movie_to_collection, name='add_movie_to_collection'),
    path('collections/<int:collection_id>/movie/<int:movie_id>/remove', views.remove_movie_from_collection,
         name='remove_movie_from_collection'),
    path('collections/<int:collection_id>/remove', views.remove_collection, name='remove_collection')
]
