# movies/models.py

from django.db import models
from django.conf import settings


class Movie(models.Model):
    """
    영화 모델
    TMDB에서 가져온 영화 정보를 저장
    """
    tmdb_id = models.IntegerField(unique=True)  # TMDB 영화 ID
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)  # 줄거리
    poster_path = models.CharField(max_length=200, blank=True, null=True)  # null 허용!
    backdrop_path = models.CharField(max_length=200, blank=True, null=True)  # null 허용!
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField(default=0)  # 평점
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0)
    adult = models.BooleanField(default=False)
    genre_ids = models.JSONField(default=list)  # 장르 ID 리스트
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity']
    
    def __str__(self):
        return self.title
    
    @property
    def poster_url(self):
        """포스터 이미지 전체 URL"""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None
    
    @property
    def backdrop_url(self):
        """배경 이미지 전체 URL"""
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None


class Favorite(models.Model):
    """
    찜하기 모델
    사용자가 찜한 영화 저장
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie')  # 중복 찜하기 방지
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"