# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    """
    관리자 페이지에서 User 모델 설정
    """
    # 목록에 표시할 필드
    list_display = (
        'username',
        'email',
        'nickname',
        'is_staff',
        'is_active',
        'date_joined'
    )
    
    # 필터
    list_filter = ('is_staff', 'is_active', 'date_joined')
    
    # 검색
    search_fields = ('username', 'email', 'nickname')
    
    # UserAdmin의 fieldsets에 nickname 추가
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('nickname', 'profile_image')}),
    )
    
    # 유저 생성 시 nickname도 입력받기
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('추가 정보', {'fields': ('nickname',)}),
    )

# User 모델을 관리자 페이지에 등록
admin.site.register(User, CustomUserAdmin)