# movies/urls.py

from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # 인기 영화
    path('popular/', views.popular_movies, name='popular'),
    
    # 장르별 영화
    path('genre/<str:genre>/', views.movies_by_genre, name='by_genre'),
    
    # 영화 상세
    path('<int:movie_id>/', views.movie_detail, name='detail'),
    
    # 찜하기 토글
    path('<int:movie_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    
    # 내가 찜한 영화
    path('favorites/', views.my_favorites, name='favorites'),
]