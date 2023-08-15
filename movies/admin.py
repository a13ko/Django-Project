from django.contrib import admin
from .models import Movie , Genre , Actor ,MovieGalleryImage,MovieGalleryVideo,Language,ComingMovie,Country,Comment,Review

class MovieImageInline(admin.TabularInline):
    model = MovieGalleryImage
    extra = 1
    

class MovieVideoInline(admin.TabularInline):
    model = MovieGalleryVideo
    extra = 1
    
class MovieAdmin(admin.ModelAdmin):
    inlines = (MovieImageInline,MovieVideoInline )


admin.site.register(Movie,MovieAdmin)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Actor)
admin.site.register(Language)
admin.site.register(MovieGalleryImage)
admin.site.register(MovieGalleryVideo)
admin.site.register(ComingMovie)
admin.site.register(Country)
admin.site.register(Comment)
