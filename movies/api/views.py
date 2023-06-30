from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Movie
from .serializers import MovieSerializer,MovieCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics

@api_view()
def hello_world(request):
    movies = Movie.objects.all()
    serializers = MovieSerializer(movies,many=True)

    return Response(serializers.data)

@api_view()
def movies_detail(request,slug):
    movie = get_object_or_404(Movie,slug=slug)
    serializers = MovieSerializer(movie)
    return Response(serializers.data)

class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieCreate(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieCreateSerializer