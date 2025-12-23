# movies/tmdb_api.py

import requests
from django.conf import settings


def get_popular_movies(page=1):
    """
    인기 영화 가져오기
    """
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'ko-KR',
        'page': page
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"TMDB API 에러: {e}")
        return None


def get_movies_by_genre(genre_id, page=1):
    """
    장르별 영화 가져오기
    """
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'ko-KR',
        'with_genres': genre_id,
        'page': page,
        'sort_by': 'popularity.desc'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"TMDB API 에러: {e}")
        return None


def get_movie_detail(movie_id):
    """
    영화 상세 정보 가져오기 (TMDB ID)
    예고편과 출연진 정보 포함
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'ko-KR',
        'append_to_response': 'videos,credits'  # 예고편과 출연진 정보 포함
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"TMDB API 에러: {e}")
        return None


def get_movie_videos(movie_id):
    """
    영화 예고편 가져오기
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'ko-KR'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 한국어 예고편이 없으면 영어 예고편 가져오기
        if not data.get('results'):
            params['language'] = 'en-US'
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"TMDB API 에러: {e}")
        return None


def get_movie_credits(movie_id):
    """
    영화 출연진 및 제작진 정보 가져오기
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'ko-KR'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"TMDB API 에러: {e}")
        return None


def search_movies(query, page=1):
    """
    영화 검색
    """
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'ko-KR',
        'query': query,
        'page': page
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"TMDB API 에러: {e}")
        return None


def get_genres():
    """
    장르 목록 가져오기
    """
    url = "https://api.themoviedb.org/3/genre/movie/list"
    params = {
        'api_key': settings.TMDB_API_KEY,
        'language': 'ko-KR'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"TMDB API 에러: {e}")
        return None


# 장르 ID 매핑
GENRE_MAP = {
    'action': 28,
    'comedy': 35,
    'romance': 10749,
    'thriller': 53,
    'fantasy': 14,
    'sf': 878,
    'animation': 16
}


def get_image_url(path, size='w500'):
    """
    TMDB 이미지 URL 생성
    size: w92, w154, w185, w342, w500, w780, original
    """
    if not path:
        return None
    return f"https://image.tmdb.org/t/p/{size}{path}"