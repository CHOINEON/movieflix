# movies/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Movie, Favorite
from .serializers import MovieSerializer, FavoriteSerializer
from .tmdb_api import (
    get_popular_movies, 
    get_movies_by_genre, 
    get_movie_detail,
    get_movie_videos,
    get_movie_credits,
    GENRE_MAP
)
from django.conf import settings
import json

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


@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, tmdb_id):
    """
    영화 상세 정보 (TMDB ID 사용)
    GET /api/movies/detail/<tmdb_id>/
    
    예고편, 출연진, 감독 정보 포함
    """
    # TMDB에서 상세 정보 가져오기
    tmdb_data = get_movie_detail(tmdb_id)
    
    if not tmdb_data:
        return Response(
            {'error': '영화 정보를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # DB에 저장 또는 업데이트
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
    
    # 예고편 정보 추출
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
    
    # 출연진 및 감독 정보 추출
    credits = tmdb_data.get('credits', {})
    cast = credits.get('cast', [])[:10]  # 상위 10명만
    crew = credits.get('crew', [])
    
    directors = [
        {'name': person['name'], 'profile_path': person.get('profile_path')}
        for person in crew if person.get('job') == 'Director'
    ]
    
    # 장르 정보
    genres = [genre['name'] for genre in tmdb_data.get('genres', [])]
    
    # 찜하기 상태 확인
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(
            user=request.user,
            movie=movie
        ).exists()
    
    # 응답 데이터 구성
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
@csrf_exempt
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
        
        system_prompt = f"""당신은 피곤하고 전문적인 영화 추천 AI 어시스턴트입니다.

**사용자 정보:**
- 사용자 이름: {user.username}
- 찜한 영화 목록:
{favorite_movies_text}

**역할:**
- 사용자의 영화 취향을 파악하여 맞춤 추천을 제공합니다
- 영화에 대한 질문에 까칠하지만 츤데레 선배처럼 상세하게 답변합니다
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