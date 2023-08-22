from django.db import models
from django.db.models import Count
from services.choiches import account
from services.mixin import SlugMixin, DateMixin
from services.slugify import slugify
from services.generator import CodeGenerator
from services.uploader import Uploader

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model


User = get_user_model()


class Country(DateMixin):
    name = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        verbose_name = 'Ölkə'
        verbose_name_plural = 'Ölkə'

    def __str__(self):
        return self.name



class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Janr'
        verbose_name_plural = 'Janr'

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



class Language(DateMixin):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Dil'
        verbose_name_plural = 'Dillər'

    def __str__(self):
        return self.name


class Serie(SlugMixin,DateMixin):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    account = models.CharField(max_length=30,choices=account,default='Basic')
    release_date = models.DateField()
    description = RichTextField()
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    trailer = models.URLField(blank=True, null=True)
    poster = models.ImageField(upload_to='posters/')
    language = models.ManyToManyField(Language)
    imdb = models.FloatField(default=2.1)
    country = models.ForeignKey(Country, on_delete=models.PROTECT,blank=True,null=True)
    age_limit = models.PositiveIntegerField(blank=True,null=True)
    wishlist = models.ManyToManyField(User, blank=True)


    class Meta:
        verbose_name = 'Serial'
        verbose_name_plural = 'Seriallar'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.code = CodeGenerator.create_slug_shortcode(
            size=20, model_=Serie
        )
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Season(DateMixin):
    number = models.IntegerField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE,related_name='seasons')

    class Meta:
        verbose_name = 'Sezon'
        verbose_name_plural = 'Sezon'

    def __str__(self):
        return f"{self.serie.title} - Season {self.number}"
    @property
    def count_episodes(self):
        return Episode.objects.filter(season=self).count()

class Episode(SlugMixin,DateMixin):
    title = models.CharField(max_length=255)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    episode_number = models.IntegerField()
    release_date = models.DateField()
    description = RichTextField()
    duration = models.DurationField()
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE,blank=True,null=True)
    watched_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Bölüm'
        verbose_name_plural = 'Bölümlər'

    def __str__(self):
        return f"{self.season.serie.title} - S{self.season.number:02d}E{self.episode_number:02d}: {self.title}"

    def save(self, *args, **kwargs):
        self.code = CodeGenerator.create_slug_shortcode(
            size=20, model_= Serie
        )
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Review(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tv_series_reviews')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)])
    title = models.TextField(default="null")
    text = RichTextField(default="null")
    
    class Meta:
        verbose_name = 'Serial Reyting'
        verbose_name_plural = 'Serial Reyting'
    
    def __str__(self):
        return f'{self.user.username} - {self.serie.title}'

class EpisodeReview(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tv_episodes_reviews')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)])
    title = models.TextField(default="null")
    text = RichTextField(default="null")
    
    class Meta:
        verbose_name = 'Epizod Reyting'
        verbose_name_plural = 'Epizod Reyting'
    
    def __str__(self):
        return f'{self.user.username} - {self.episode.title}'



class Comment(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tv_series_comments')
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    comment = RichTextField()
    likes = models.ManyToManyField(User, related_name='tv_series_liked_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='tv_series_disliked_comments', blank=True)  

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Commentlər'

    def __str__(self):
        return f'{self.user.username} - {self.serie.title}'

    def can_delete(self, user):
        return self.user == user


class CommentEpisode(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='commentler')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    commentepisode = RichTextField()
    likes = models.ManyToManyField(User, related_name='tv_episodes_liked_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='tv_episodes_disliked_comments', blank=True)  

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Bolum Comment'



    def __str__(self):
        return f'{self.user.username} - {self.episode.title} '


    
    def can_delete(self, user):
        return self.user == user
    



class SerieGallery(DateMixin):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Uploader.upload_image_serie)

    class Meta:
        verbose_name = 'Şəkil'
        verbose_name_plural = 'Şəkillər'

    def __str__(self):
        return self.serie.title


class EpisodeGallery(DateMixin):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    video = models.FileField(upload_to=Uploader.upload_video_episode)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videolar'

    def __str__(self):
        return self.episode.title