# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# 현재 프로젝트의 User 모델 가져오기
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    유저 정보를 보여줄 때 사용
    비밀번호는 보여주지 않음
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'profile_image')
        read_only_fields = ('id',)  # id는 읽기만 가능


class SignupSerializer(serializers.ModelSerializer):
    """
    회원가입할 때 사용
    """
    password = serializers.CharField(
        write_only=True,          # 응답에는 포함하지 않음
        required=True,
        validators=[validate_password]  # Django 비밀번호 검증
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password_confirmation',
            'email',
            'nickname'
        )

    def validate(self, attrs):
        """
        비밀번호 일치 확인
        """
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({
                "password": "비밀번호가 일치하지 않습니다."
            })
        return attrs

    def create(self, validated_data):
        """
        유저 생성
        password_confirmation은 제거하고 저장
        """
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    로그인할 때 사용
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True
    )