# backend/movies/admin.py

from django.contrib import admin
from .models import Movie, Favorite, Review, ReviewLike


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'tmdb_id', 'vote_average', 'release_date', 'popularity']
    list_filter = ['adult', 'release_date']
    search_fields = ['title', 'original_title']
    ordering = ['-popularity']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'movie__title']
    ordering = ['-created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'is_spoiler', 'created_at']
    list_filter = ['rating', 'is_spoiler', 'created_at']
    search_fields = ['user__username', 'movie__title', 'content']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'review__movie__title']
    ordering = ['-created_at']