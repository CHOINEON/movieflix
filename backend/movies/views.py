# backend/movies/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Movie, Favorite, Review, ReviewLike
from .serializers import (
    MovieSerializer, FavoriteSerializer, 
    ReviewSerializer, ReviewCreateUpdateSerializer
)
from .tmdb_api import (
    get_popular_movies, 
    get_movies_by_genre, 
    get_movie_detail,
    GENRE_MAP
)
from django.conf import settings
import json

@api_view(['GET'])
@permission_classes([AllowAny])
def popular_movies(request):
    """인기 영화 목록"""
    page = request.GET.get('page', 1)
    data = get_popular_movies(page=page)
    
    if not data:
        return Response(
            {'error': 'TMDB API 호출 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
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
    
    serializer = MovieSerializer(movies, many=True, context={'request': request})
    
    return Response({
        'page': data.get('page'),
        'total_pages': data.get('total_pages'),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def movies_by_genre(request, genre):
    """장르별 영화 목록"""
    page = request.GET.get('page', 1)
    genre_id = GENRE_MAP.get(genre.lower())
    
    if not genre_id:
        return Response(
            {'error': '유효하지 않은 장르입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    data = get_movies_by_genre(genre_id, page=page)
    
    if not data:
        return Response(
            {'error': 'TMDB API 호출 실패'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
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
    
    serializer = MovieSerializer(movies, many=True, context={'request': request})
    
    return Response({
        'genre': genre,
        'page': data.get('page'),
        'total_pages': data.get('total_pages'),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, tmdb_id):
    """영화 상세 정보"""
    tmdb_data = get_movie_detail(tmdb_id)
    
    if not tmdb_data:
        return Response(
            {'error': '영화 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    movie, created = Movie.objects.update_or_create(
        tmdb_id=tmdb_data['id'],
        defaults={
            'title': tmdb_data.get('title', ''),
            'original_title': tmdb_data.get('original_title', ''),
            'overview': tmdb_data.get('overview', ''),
            'poster_path': tmdb_data.get('poster_path', ''),
            'backdrop_path': tmdb_data.get('backdrop_path', ''),
            'release_date': tmdb_data.get('release_date'),
            'vote_average': tmdb_data.get('vote_average', 0),
            'vote_count': tmdb_data.get('vote_count', 0),
            'popularity': tmdb_data.get('popularity', 0),
            'adult': tmdb_data.get('adult', False),
            'genre_ids': [g['id'] for g in tmdb_data.get('genres', [])]
        }
    )
    
    videos = tmdb_data.get('videos', {}).get('results', [])
    trailer = None
    for video in videos:
        if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
            trailer = {
                'key': video.get('key'),
                'name': video.get('name'),
                'youtube_url': f"https://www.youtube.com/embed/{video.get('key')}"
            }
            break
    
    credits = tmdb_data.get('credits', {})
    cast = credits.get('cast', [])[:10]
    crew = credits.get('crew', [])
    
    directors = [
        {'name': person['name'], 'profile_path': person.get('profile_path')}
        for person in crew if person.get('job') == 'Director'
    ]
    
    genres = [genre['name'] for genre in tmdb_data.get('genres', [])]
    
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, movie=movie).exists()
    
    response_data = {
        'id': movie.id,
        'tmdb_id': movie.tmdb_id,
        'title': movie.title,
        'original_title': movie.original_title,
        'overview': movie.overview,
        'poster_url': movie.poster_url,
        'backdrop_url': movie.backdrop_url,
        'release_date': movie.release_date,
        'vote_average': movie.vote_average,
        'vote_count': movie.vote_count,
        'runtime': tmdb_data.get('runtime'),
        'genres': genres,
        'trailer': trailer,
        'cast': [
            {
                'name': actor['name'],
                'character': actor.get('character'),
                'profile_path': f"https://image.tmdb.org/t/p/w185{actor['profile_path']}" if actor.get('profile_path') else None
            }
            for actor in cast
        ],
        'directors': directors,
        'is_favorited': is_favorited
    }
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request, movie_id):
    """찜하기 토글"""
    movie = get_object_or_404(Movie, id=movie_id)
    
    favorite = Favorite.objects.filter(user=request.user, movie=movie).first()
    
    if favorite:
        favorite.delete()
        return Response({
            'message': '찜하기가 취소되었습니다.',
            'is_favorited': False
        })
    else:
        Favorite.objects.create(user=request.user, movie=movie)
        return Response({
            'message': '찜하기가 완료되었습니다.',
            'is_favorited': True
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_favorites(request):
    """내가 찜한 영화 목록"""
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)


# ==================== 리뷰 API ====================

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # GET은 누구나, POST는 내부에서 체크
def movie_reviews(request, movie_id):
    """
    영화 리뷰 목록 조회 / 리뷰 작성
    GET /api/movies/<movie_id>/reviews/ - 누구나 조회 가능
    POST /api/movies/<movie_id>/reviews/ - 로그인한 사용자만 작성 가능
    """
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'GET':
        # 리뷰 목록 조회 - 누구나 가능
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # 디버깅 로그
        print(f"🔍 POST 요청 받음")
        print(f"🔍 사용자: {request.user}")
        print(f"🔍 인증 여부: {request.user.is_authenticated}")
        print(f"🔍 세션 키: {request.session.session_key}")
        print(f"🔍 쿠키: {request.COOKIES}")
        
        # 리뷰 작성 - 로그인 필요
        if not request.user.is_authenticated:
            return Response(
                {'error': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 이미 리뷰를 작성했는지 확인
        existing_review = Review.objects.filter(user=request.user, movie=movie).first()
        if existing_review:
            return Response(
                {'error': '이미 이 영화에 리뷰를 작성하셨습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReviewCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, movie=movie)
            response_serializer = ReviewSerializer(review, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def review_detail(request, review_id):
    """
    리뷰 수정 / 삭제
    """
    review = get_object_or_404(Review, id=review_id)
    
    # 본인의 리뷰인지 확인
    if review.user != request.user:
        return Response(
            {'error': '본인의 리뷰만 수정/삭제할 수 있습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'PUT':
        serializer = ReviewCreateUpdateSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = ReviewSerializer(review, context={'request': request})
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(
            {'message': '리뷰가 삭제되었습니다.'},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_review_like(request, review_id):
    """리뷰 좋아요 토글"""
    review = get_object_or_404(Review, id=review_id)
    
    # 자기 리뷰에는 좋아요 불가
    if review.user == request.user:
        return Response(
            {'error': '본인의 리뷰에는 좋아요를 누를 수 없습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    like = ReviewLike.objects.filter(user=request.user, review=review).first()
    
    if like:
        like.delete()
        return Response({
            'message': '좋아요가 취소되었습니다.',
            'is_liked': False,
            'likes_count': review.likes.count()
        })
    else:
        ReviewLike.objects.create(user=request.user, review=review)
        return Response({
            'message': '좋아요!',
            'is_liked': True,
            'likes_count': review.likes.count()
        }, status=status.HTTP_201_CREATED)



@csrf_exempt
@api_view(['POST'])
def ai_chat(request):
    """
    AI 챗봇과 대화하며 영화 추천받기
    
    """
    print("=" * 80)
    print("🚀 [ai_chat] 함수 호출됨!")
    print(f"👤 [ai_chat] 사용자: {request.user}")
    print(f"🔐 [ai_chat] 인증 여부: {request.user.is_authenticated}")
    print("=" * 80)
    
    # 수동으로 인증 확인
    if not request.user.is_authenticated:
        print("❌ [ai_chat] 인증되지 않은 사용자")
        return Response(
            {'error': '로그인이 필요합니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    user_message = request.data.get('message', '')
    print(f"📝 [ai_chat] 받은 메시지: '{user_message}'")

    if not user_message:
        print("❌ [ai_chat] 메시지가 비어있음")
        return Response(
            {'error': '메시지를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        print("🔧 [ai_chat] Anthropic 클라이언트 초기화 시작")
        from anthropic import Anthropic

        # GMS API 키 확인
        api_key = settings.GMS_API_KEY
        print(f"🔑 [ai_chat] API 키 존재: {bool(api_key)}")
        
        if not api_key:
            print("❌ [ai_chat] API 키 없음")
            return Response(
                {'error': 'GMS API 키가 설정되지 않았습니다.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        print(f"🌐 [ai_chat] GMS URL: {settings.GMS_BASE_URL}")
        client = Anthropic(
            api_key=api_key,
            base_url=settings.GMS_BASE_URL
        )
        print("✅ [ai_chat] 클라이언트 초기화 완료")

        # 사용자 컨텍스트 수집
        user = request.user
        favorites = user.favorites.select_related('movie').all()[:10]
        print(f"🎬 [ai_chat] 찜한 영화: {favorites.count()}개")

        favorite_movies_text = ""
        if favorites:
            favorite_list = [
                f"- {fav.movie.title} ({fav.movie.release_date.year if fav.movie.release_date else 'N/A'})"
                for fav in favorites
            ]
            favorite_movies_text = "\n".join(favorite_list)
        else:
            favorite_movies_text = "아직 찜한 영화가 없습니다."
        
        system_prompt = f"""당신은 연상의 전문적인 영화 추천 AI 어시스턴트입니다.

**사용자 정보:**
- 사용자 이름: {user.username}
- 찜한 영화 목록:
{favorite_movies_text}

**역할:**
- 사용자의 영화 취향을 파악하여 맞춤 추천을 제공합니다
- 영화에 대한 질문에 예의는 지키지만 줏대있는선배처럼 상세하게 답변합니다
- 구체적인 이유와 함께 영화를 추천합니다
- 한국어로 자연스럽게 대화합니다

**가이드라인:**
- 찜한 영화 목록을 참고하여 취향을 고려한 추천을 합니다
- 영화 제목은 **굵게** 표시합니다
- 추천 시 장르, 감독, 주연배우 등을 언급합니다
- 간결하면서도 유용한 정보를 제공합니다
- 3개의 영화를 추천합니다"""
        
        print("🤖 [ai_chat] Claude API 호출 시작")
        message = client.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        
        print("✅ [ai_chat] Claude 응답 받음")
        ai_response = message.content[0].text
        print(f"💬 [ai_chat] 응답 길이: {len(ai_response)}자")
        
        return Response({
            'response': ai_response,
            'user_message': user_message
        })
        
    except Exception as e:
        import traceback
        print("=" * 80)
        print("❌ [ai_chat] 오류 발생")
        print(f"오류: {str(e)}")
        print(traceback.format_exc())
        print("=" * 80)
        
        return Response(
            {'error': f'AI 서비스 오류: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )