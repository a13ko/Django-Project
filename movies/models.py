from django.db import models

from services.mixin import SlugMixin, DateMixin
from services.slugify import slugify
from services.generator import CodeGenerator
from services.uploader import Uploader
from services.choiches import account

from ckeditor.fields import RichTextField

from django.db import models
from django.contrib.auth import get_user_model



# Create your models here.
User = get_user_model()



class Country(DateMixin):
    name = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        verbose_name = 'Ölkə'
        verbose_name_plural = 'Ölkə'

    def __str__(self):
        return self.name

class Genre(DateMixin):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Janr'
        verbose_name_plural = 'Janr'

    def __str__(self):
        return self.name

class Language(DateMixin):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Dil'
        verbose_name_plural = 'Dillər'

    def __str__(self):
        return self.name

class Actor(DateMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()

    class Meta:
        verbose_name = 'Aktyor'
        verbose_name_plural = 'Aktyorlar'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Movie(SlugMixin,DateMixin):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    description = RichTextField()
    account = models.CharField(max_length=30,choices=account,default='Basic')
    release_date = models.DateField()
    running_time = models.PositiveIntegerField()
    age_limit = models.PositiveIntegerField(blank=True,null=True)
    language = models.ManyToManyField(Language)
    imdb = models.FloatField()
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    country = models.ForeignKey(Country, on_delete=models.PROTECT,blank=True,null=True)
    trailer = models.URLField(blank=True, null=True)
    poster = models.ImageField(upload_to='posters/')
    wishlist = models.ManyToManyField(User, blank=True)
    watched_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Film'
        verbose_name_plural = 'Filmlər'
    

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.code = CodeGenerator.create_slug_shortcode(
            size=20, model_=Movie
        )
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)





class Comment(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = RichTextField()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Commentlər'



    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'


    
    def can_delete(self, user):
        return self.user == user
    






class ComingMovie(DateMixin):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre)
    poster = models.ImageField(upload_to='posters/')

    class Meta:
        verbose_name = 'Gələcək Filmlər'
        verbose_name_plural = 'Gələcək Filmlər'

    def __str__(self):
        return self.title

        




class MovieGalleryVideo(DateMixin):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    video = models.FileField(upload_to=Uploader.upload_video_movies)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videolar'

    def __str__(self):
        return self.movie.title


class MovieGalleryImage(DateMixin):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Uploader.upload_image_movies)

    class Meta:
        verbose_name = 'Şəkil'
        verbose_name_plural = 'Şəkillər'

    def __str__(self):
        return self.movie.title
    

