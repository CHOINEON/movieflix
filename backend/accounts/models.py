# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    커스텀 유저 모델
    Django 기본 User에 추가 필드를 넣을 수 있음
    """
    # AbstractUser가 이미 username, password, email 등을 가지고 있음
    
    # 추가 필드
    nickname = models.CharField(max_length=50, unique=True)
    profile_image = models.ImageField(
        upload_to='profiles/',  # 프로필 이미지는 profiles/ 폴더에 저장
        null=True,              # 필수 아님
        blank=True              # 빈 값 허용
    )
    
    def __str__(self):
        return self.username