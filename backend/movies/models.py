# backend/movies/models.py

from django.db import models
from django.conf import settings


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    poster_path = models.CharField(max_length=200, blank=True, null=True)
    backdrop_path = models.CharField(max_length=200, blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0)
    adult = models.BooleanField(default=False)
    genre_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None

    @property
    def backdrop_url(self):
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None

    class Meta:
        ordering = ['-popularity']


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Review(models.Model):
    """영화 리뷰 모델"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],  # 1~5점
        help_text='별점 (1-5)'
    )
    content = models.TextField(
        max_length=2000,
        help_text='리뷰 내용 (최대 2000자)'
    )
    is_spoiler = models.BooleanField(
        default=False,
        help_text='스포일러 포함 여부'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')  # 한 사용자당 영화 1개 리뷰만
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}점)"


class ReviewLike(models.Model):
    """리뷰 좋아요 모델"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='review_likes'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')  # 한 사용자당 리뷰 1개만 좋아요
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.review}"