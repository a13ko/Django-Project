from django.urls import path
from .views import *

app_name = "movies"


urlpatterns = [
    path("",show_home, name="home"),
    path("movies/",show_list, name="movies"),
    path("movies-detail/<slug>/",movie_details, name="movies-detail"),
    path('delete-comment/', delete_comment, name='delete_comment'),
    path("movie-wish/",movie_wish_view, name="movie-wish"),
    path("wishlist/",wishlist_view, name="wishlist"),
    path("movie-serie/",movie_serie, name="movie-serie"),
    
    
]