from django.urls import path
from .views import *

app_name = "products_api"

urlpatterns = [
    path("movies/", MovieList.as_view(), name="movie-list"),
    path("create/", MovieCreate.as_view(), name="create"),
    path("detail/<slug>/", movies_detail, name="detail"),
]
