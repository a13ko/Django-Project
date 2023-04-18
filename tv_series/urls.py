from django.urls import path
from .views import *

app_name = "series"


urlpatterns = [
    path("series/",show_list_series, name="series"),
    path("serie-wish/",serie_wish_view, name="serie-wish"),
    path("series-detail/<slug>/",serie_detail, name="series-detail"),
    path("series-episode/",serie_episode, name="series-episode"),
    path('delete-comments/', delete_comment, name='delete_comments'),
    path('delete-commentss/', delete_comments, name='delete_commentss'),
    

]