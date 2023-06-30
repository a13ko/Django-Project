from rest_framework import serializers
from ..models import *

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name",)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("first_name","last_name")

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name","account")

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("name",)

class MovieSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)
    wishlist = WishlistSerializer(many=True)
    language = LanguageSerializer(many=True)
    class Meta:
        model = Movie
        fields = "__all__"

class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"
        