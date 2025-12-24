# backend/movies/urls.py

from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 인기 영화
    path('popular/', views.popular_movies, name='popular'),
    
    # 장르별 영화
    path('genre/<str:genre>/', views.movies_by_genre, name='genre'),
    
    # 영화 상세 정보 (TMDB ID)
    path('detail/<int:tmdb_id>/', views.movie_detail, name='detail'),
    
    # 찜하기 토글
    path('<int:movie_id>/favorite/', views.toggle_favorite, name='favorite'),
    
    # 내가 찜한 영화
    path('favorites/', views.my_favorites, name='favorites'),
    
    # 리뷰 관련
    path('<int:movie_id>/reviews/', views.movie_reviews, name='movie_reviews'),  # 리뷰 목록 / 작성
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),  # 리뷰 수정 / 삭제
    path('reviews/<int:review_id>/like/', views.toggle_review_like, name='review_like'),  # 리뷰 좋아요
]