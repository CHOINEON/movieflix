# movies/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Movie, Favorite
from .serializers import MovieSerializer, FavoriteSerializer
from .tmdb_api import get_popular_movies, get_movies_by_genre, GENRE_MAP


@api_view(['GET'])
@permission_classes([AllowAny])
def popular_movies(request):
    """
    인기 영화 목록
    GET /api/movies/popular/
    """
    page = request.GET.get('page', 1)
    
    # TMDB에서 영화 데이터 가져오기
    data = get_popular_movies(page=page)
    
    if not data:
        return Response(
            {'error': 'TMDB API 호출 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # 영화 데이터를 DB에 저장 (없으면 생성)
    movies = []
    for movie_data in data.get('results', []):
        movie, created = Movie.objects.update_or_create(
            tmdb_id=movie_data['id'],
            defaults={
                'title': movie_data.get('title', ''),
                'original_title': movie_data.get('original_title', ''),
                'overview': movie_data.get('overview', ''),
                'poster_path': movie_data.get('poster_path', ''),
                'backdrop_path': movie_data.get('backdrop_path', ''),
                'release_date': movie_data.get('release_date'),
                'vote_average': movie_data.get('vote_average', 0),
                'vote_count': movie_data.get('vote_count', 0),
                'popularity': movie_data.get('popularity', 0),
                'adult': movie_data.get('adult', False),
                'genre_ids': movie_data.get('genre_ids', [])
            }
        )
        movies.append(movie)
    
    # Serialize
    serializer = MovieSerializer(
        movies,
        many=True,
        context={'request': request}
    )
    
    return Response({
        'page': data.get('page'),
        'total_pages': data.get('total_pages'),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def movies_by_genre(request, genre):
    """
    장르별 영화 목록
    GET /api/movies/genre/<genre>/
    genre: action, comedy, romance, thriller, fantasy, sf, animation
    """
    page = request.GET.get('page', 1)
    
    # 장르 ID 가져오기
    genre_id = GENRE_MAP.get(genre.lower())
    
    if not genre_id:
        return Response(
            {'error': '유효하지 않은 장르입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # TMDB에서 영화 데이터 가져오기
    data = get_movies_by_genre(genre_id, page=page)
    
    if not data:
        return Response(
            {'error': 'TMDB API 호출 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # 영화 데이터를 DB에 저장
    movies = []
    for movie_data in data.get('results', []):
        movie, created = Movie.objects.update_or_create(
            tmdb_id=movie_data['id'],
            defaults={
                'title': movie_data.get('title', ''),
                'original_title': movie_data.get('original_title', ''),
                'overview': movie_data.get('overview', ''),
                'poster_path': movie_data.get('poster_path', ''),
                'backdrop_path': movie_data.get('backdrop_path', ''),
                'release_date': movie_data.get('release_date'),
                'vote_average': movie_data.get('vote_average', 0),
                'vote_count': movie_data.get('vote_count', 0),
                'popularity': movie_data.get('popularity', 0),
                'adult': movie_data.get('adult', False),
                'genre_ids': movie_data.get('genre_ids', [])
            }
        )
        movies.append(movie)
    
    # Serialize
    serializer = MovieSerializer(
        movies,
        many=True,
        context={'request': request}
    )
    
    return Response({
        'genre': genre,
        'page': data.get('page'),
        'total_pages': data.get('total_pages'),
        'results': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt  # ← 이 한 줄만 추가!
def toggle_favorite(request, movie_id):
    """
    찜하기 토글
    POST /api/movies/<movie_id>/favorite/
    """
    movie = get_object_or_404(Movie, id=movie_id)
    
    # 이미 찜했는지 확인
    favorite = Favorite.objects.filter(
        user=request.user,
        movie=movie
    ).first()
    
    if favorite:
        # 찜 취소
        favorite.delete()
        return Response({
            'message': '찜하기가 취소되었습니다.',
            'is_favorited': False
        })
    else:
        # 찜하기
        Favorite.objects.create(
            user=request.user,
            movie=movie
        )
        return Response({
            'message': '찜하기가 완료되었습니다.',
            'is_favorited': True
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_favorites(request):
    """
    내가 찜한 영화 목록
    GET /api/movies/favorites/
    """
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, movie_id):
    """
    영화 상세 정보
    GET /api/movies/<movie_id>/
    """
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = MovieSerializer(movie, context={'request': request})
    
    return Response(serializer.data)