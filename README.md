# 🎬 FilmIn

> 감상한 영화의 배경지식을 추천하는 AI 기반 영화 플랫폼

<br>

## 📌 프로젝트 소개

**FilmIn**은 사용자의 취향을 분석하여 맞춤형 영화를 추천하고, AI를 활용해 영화 배경지식과 심도 있는 추천을 제공하는 웹 서비스입니다.

### 주요 특징
- 🤖 **AI 영화 추천**: Claude AI를 활용한 개인화된 영화 추천
- 🎯 **취향 기반 필터링**: 장르별 영화 탐색 및 검색
- ⭐ **리뷰 시스템**: 영화 리뷰 작성, 수정, 삭제 및 좋아요 기능
- 💬 **AI 챗봇**: 실시간 영화 추천 대화
- 👥 **소셜 기능**: 사용자 팔로우 및 찜하기

<br>

## 🛠 기술 스택

### Frontend
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![Pinia](https://img.shields.io/badge/Pinia-FFD859?style=for-the-badge&logo=pinia&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white)

### Backend
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

### AI & External APIs
![Claude AI](https://img.shields.io/badge/Claude_AI-7C3AED?style=for-the-badge&logo=anthropic&logoColor=white)
![TMDB](https://img.shields.io/badge/TMDB-01B4E4?style=for-the-badge&logo=themoviedatabase&logoColor=white)

<br>

## 📂 프로젝트 구조

```
final-pjt/
├── backend/                    # Django 백엔드
│   ├── accounts/              # 사용자 인증 앱
│   ├── movies/                # 영화 관련 앱
│   │   ├── models.py         # Movie, Review, Favorite 모델
│   │   ├── views.py          # API 뷰
│   │   ├── serializers.py    # DRF Serializers
│   │   └── tmdb_api.py       # TMDB API 연동
│   └── movie_project/         # 프로젝트 설정
│
└── frontend/                   # Vue.js 프론트엔드
    ├── src/
    │   ├── api/               # API 통신 모듈
    │   ├── components/        # Vue 컴포넌트
    │   ├── stores/            # Pinia 스토어
    │   ├── views/             # 페이지 뷰
    │   └── router/            # Vue Router 설정
    └── public/
```

<br>

## 🗄️ ERD (Entity Relationship Diagram)

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│    User     │         │    Movie    │         │    Actor    │
├─────────────┤         ├─────────────┤         ├─────────────┤
│ id          │         │ id          │         │ id          │
│ username    │◄───┐    │ tmdb_id     │◄───┐    │ name        │
│ email       │    │    │ title       │    │    └─────────────┘
│ nickname    │    │    │ overview    │    │           │
└─────────────┘    │    │ poster_path │    │           │
       │           │    │ release_date│    │    ┌──────▼──────┐
       │           │    │ vote_average│    │    │ MovieActor  │
       │           │    └─────────────┘    │    │  (N:M)      │
       │           │           │           │    └─────────────┘
       │           │           │           │
       │      ┌────▼─────┐     │      ┌────▼────────┐
       │      │ Favorite │     │      │   Review    │
       │      │   (N:M)  │     │      ├─────────────┤
       │      └──────────┘     │      │ id          │
       │                       │      │ content     │
       │                       │      │ rating      │
       │                       └──────┤ is_spoiler  │
       │                              │ created_at  │
       │                              └─────────────┘
       │                                     │
       │                              ┌──────▼──────┐
       └──────────────────────────────┤ ReviewLike  │
                                      │   (N:M)     │
                                      └─────────────┘
```

<br>

## 🚀 시작하기

### 사전 요구사항
- Python 3.8+
- Node.js 16+
- Git


### 2️⃣ 백엔드 설정

```bash
cd backend

# 가상환경 생성 및 활성화 (Windows)
python -m venv venv
venv\Scripts\activate

# 가상환경 생성 및 활성화 (Mac/Linux)
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt


# 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser

# 서버 실행
python manage.py runserver
```

### 3️⃣ 프론트엔드 설정

```bash
cd frontend

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```



<br>

## 📡 주요 API 엔드포인트

### 인증
- `POST /api/accounts/signup/` - 회원가입
- `POST /api/accounts/login/` - 로그인
- `POST /api/accounts/logout/` - 로그아웃
- `GET /api/accounts/user/` - 사용자 정보 조회

### 영화
- `GET /api/movies/popular/` - 인기 영화 목록
- `GET /api/movies/genre/<genre>/` - 장르별 영화 목록
- `GET /api/movies/detail/<tmdb_id>/` - 영화 상세 정보
- `POST /api/movies/<movie_id>/favorite/` - 찜하기 토글
- `GET /api/movies/favorites/` - 내가 찜한 영화

### 리뷰
- `GET /api/movies/<movie_id>/reviews/` - 리뷰 목록 조회
- `POST /api/movies/<movie_id>/reviews/` - 리뷰 작성
- `PUT /api/movies/reviews/<review_id>/` - 리뷰 수정
- `DELETE /api/movies/reviews/<review_id>/` - 리뷰 삭제
- `POST /api/movies/reviews/<review_id>/like/` - 리뷰 좋아요

### AI 챗봇
- `POST /api/movies/ai-chat/` - AI 영화 추천 대화

<br>

## 🎯 주요 기능

### 1. 영화 탐색 및 검색
- TMDB API를 활용한 실시간 영화 데이터
- 장르별 필터링
- 인기도 순 정렬

### 2. AI 영화 추천
- Claude AI 기반 개인화 추천
- 사용자 찜 목록 분석
- 자연어 대화를 통한 추천

### 3. 리뷰 시스템
- 영화별 리뷰 작성 (평점 + 텍스트)
- 리뷰 좋아요 기능
- 본인 리뷰 수정/삭제

### 4. 소셜 기능
- 영화 찜하기
- 영화 리뷰 CRUD

<br>

## 🎨 화면 구성

### 주요 페이지
- **홈** (`/`) - 인기 영화 및 추천 영화
- **영화 목록** (`/movies`) - 전체 영화 탐색
- **영화 상세** (`/movies/:id`) - 상세 정보 및 리뷰
- **AI 챗봇** (`/chatbot`) - AI 영화 추천
- **찜 목록** (`/favorites`) - 내가 찜한 영화


<br>

## 🔐 보안

- Django Session 인증
- CSRF 토큰 검증
- 본인 리뷰만 수정/삭제 가능
- 환경변수를 통한 API 키 관리

<br>

## 📝 개발 가이드

### 코드 스타일
- **Backend**: PEP 8 (Python)
- **Frontend**: ESLint + Prettier

### Git 브랜치 전략
- `master` - 메인
- `main` - 배포 브랜치(예정)
- `feature_chat` - 개발 브랜치

### 커밋 메시지 컨벤션
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 코드
chore: 빌드 업무, 패키지 매니저 설정
```

<br>

## 🐛 트러블슈팅

### 마이그레이션 오류
```bash
# 마이그레이션 초기화
python manage.py migrate --run-syncdb

# 또는
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### CORS 오류
- `settings.py`에서 `CORS_ALLOWED_ORIGINS` 확인
- 프론트엔드 URL이 포함되어 있는지 확인

### CSRF 토큰 오류
- 쿠키 설정 확인 (`withCredentials: true`)
- Django `CSRF_TRUSTED_ORIGINS` 설정 확인

<br>

## 📄 라이선스

This project is licensed under the MIT License.

<br>

## 👥 팀원

| 이름 | 역할 | GitHub |
|------|------|--------|
| 팀원1 | FE,BE | [조혜린](https://github.com/username1) |
| 팀원2 | FE,AI | [최혜진](https://github.com/CHOINEON) |

<br>


---

**Made with ❤️ by FilmIn Team**