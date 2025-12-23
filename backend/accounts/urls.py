# backend/accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # CSRF 토큰 발급
    path('csrf/', views.get_csrf_token, name='csrf'),
    
    # 회원가입
    path('signup/', views.user_signup, name='signup'),
    
    # 로그인
    path('login/', views.user_login, name='login'),
    
    # 로그아웃
    path('logout/', views.user_logout, name='logout'),
    
    # 사용자 정보
    path('user/', views.user_info, name='user'),
    
    # 프로필 업데이트
    path('profile/', views.update_profile, name='profile'),
    
    # 회원 탈퇴
    path('delete/', views.delete_account, name='delete'),
]