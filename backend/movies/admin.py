# movies/admin.py

from django.contrib import admin
from .models import Movie, Favorite


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'tmdb_id',
        'release_date',
        'vote_average',
        'popularity'
    ]
    list_filter = ['release_date', 'adult']
    search_fields = ['title', 'original_title']
    ordering = ['-popularity']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-created_at']