# movies/serializers.py

from rest_framework import serializers
from .models import Movie, Favorite


class MovieSerializer(serializers.ModelSerializer):
    """영화 Serializer"""
    poster_url = serializers.ReadOnlyField()
    backdrop_url = serializers.ReadOnlyField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'tmdb_id',
            'title',
            'original_title',
            'overview',
            'poster_path',
            'backdrop_path',
            'poster_url',
            'backdrop_url',
            'release_date',
            'vote_average',
            'vote_count',
            'popularity',
            'genre_ids',
            'is_favorited'
        ]
    
    def get_is_favorited(self, obj):
        """현재 사용자가 찜했는지 확인"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(
                user=request.user,
                movie=obj
            ).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    """찜하기 Serializer"""
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'created_at']