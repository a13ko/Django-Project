from django.contrib import admin
from .models import Season , Episode, Serie, SerieGallery,EpisodeGallery,Genre,Actor,Country,Language,Comment,CommentEpisode
# Register your models here.
class EpisodeVideoInline(admin.TabularInline):
    model = EpisodeGallery
    extra = 1
    
class EpisodeAdmin(admin.ModelAdmin):
    inlines = (EpisodeVideoInline, )

class SerieImageInline(admin.TabularInline):
    model = SerieGallery
    extra = 1
    
class SerieAdmin(admin.ModelAdmin):
    inlines = (SerieImageInline, )


admin.site.register(Season)
admin.site.register(Episode,EpisodeAdmin)
admin.site.register(Serie,SerieAdmin)
admin.site.register(EpisodeGallery)
admin.site.register(SerieGallery)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Comment)
admin.site.register(CommentEpisode)
