from django.contrib import admin

# Register your models here.
from .models import Movie, Review, Rating
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Rating)
