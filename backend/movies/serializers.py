# backend/movies/serializers.py

from rest_framework import serializers
from .models import Movie, Favorite, Review, ReviewLike


class MovieSerializer(serializers.ModelSerializer):
    poster_url = serializers.ReadOnlyField()
    backdrop_url = serializers.ReadOnlyField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'original_title', 'overview',
            'poster_path', 'backdrop_path', 'poster_url', 'backdrop_url',
            'release_date', 'vote_average', 'vote_count', 'popularity',
            'adult', 'genre_ids', 'is_favorited'
        ]

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, movie=obj).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'movie', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """리뷰 Serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'username', 'nickname', 'movie',
            'rating', 'content', 'is_spoiler',
            'likes_count', 'is_liked', 'is_mine',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        """좋아요 수"""
        return obj.likes.count()

    def get_is_liked(self, obj):
        """현재 사용자가 좋아요를 눌렀는지"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ReviewLike.objects.filter(user=request.user, review=obj).exists()
        return False

    def get_is_mine(self, obj):
        """현재 사용자의 리뷰인지"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """리뷰 생성/수정용 Serializer"""
    
    class Meta:
        model = Review
        fields = ['rating', 'content', 'is_spoiler']

    def validate_rating(self, value):
        """별점 유효성 검사"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("별점은 1~5점 사이여야 합니다.")
        return value

    def validate_content(self, value):
        """리뷰 내용 유효성 검사"""
        if len(value) > 2000:
            raise serializers.ValidationError("리뷰는 2000자를 초과할 수 없습니다.")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("리뷰는 최소 10자 이상 작성해주세요.")
        return value