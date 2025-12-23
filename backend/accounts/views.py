# backend/accounts/views.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from .models import User
from .serializers import UserSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """
    CSRF 토큰 발급
    GET /api/accounts/csrf/
    """
    # CSRF 토큰 강제 생성
    csrf_token = get_token(request)
    
    # 응답에 쿠키 설정 확인
    response = Response({
        'message': 'CSRF cookie set',
        'csrfToken': csrf_token  # 디버깅용
    })
    
    # 명시적으로 CSRF 쿠키 설정
    response.set_cookie(
        key='csrftoken',
        value=csrf_token,
        httponly=False,  # JavaScript 접근 가능
        samesite='Lax',
        secure=False  # 개발환경
    )
    
    print(f"✅ CSRF Token 발급: {csrf_token[:20]}...")
    
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def user_signup(request):
    """
    회원가입
    POST /api/accounts/signup/
    """
    username = request.data.get('username')
    email = request.data.get('email')
    nickname = request.data.get('nickname')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response(
            {'error': '모든 필드를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': '이미 존재하는 사용자 이름입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': '이미 존재하는 이메일입니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        nickname=nickname or username
    )

    login(request, user)
    
    print(f"✅ 회원가입 성공: {username}")

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    로그인
    POST /api/accounts/login/
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': '사용자 이름과 비밀번호를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 이메일로 로그인 시도
    if '@' in username:
        try:
            user_obj = User.objects.get(email=username)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
    else:
        user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        
        print(f"✅ 로그인 성공: {username}")
        print(f"📋 세션 키: {request.session.session_key}")
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': '사용자 이름 또는 비밀번호가 올바르지 않습니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def user_logout(request):
    """
    로그아웃
    POST /api/accounts/logout/
    """
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        print(f"✅ 로그아웃: {username}")
        return Response({'message': '로그아웃 되었습니다.'}, status=status.HTTP_200_OK)
    return Response({'message': '이미 로그아웃 상태입니다.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    사용자 정보
    GET /api/accounts/user/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    프로필 업데이트
    PUT /api/accounts/profile/
    """
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """
    회원 탈퇴
    DELETE /api/accounts/delete/
    """
    user = request.user
    username = user.username
    user.delete()
    print(f"✅ 회원탈퇴: {username}")
    return Response({'message': '회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)