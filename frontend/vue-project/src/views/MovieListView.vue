<!-- frontend/src/views/MovieListView.vue -->

<template>
  <div class="movie-list-view">
    <!-- 상단 네비게이션 -->
    <header class="header">
      <div class="header-left">
        <h1 class="logo">MOVIEFLIX</h1>
        
        <!-- 카테고리 드롭다운 -->
        <div class="nav-menu">
          <div class="dropdown" @click="toggleCategoryDropdown">
            <button class="dropdown-btn">
              카테고리
              <span class="arrow" :class="{ 'open': showCategoryDropdown }">▼</span>
            </button>
            
            <div v-if="showCategoryDropdown" class="dropdown-menu">
              <a 
                v-for="category in categories" 
                :key="category.id"
                @click="selectCategory(category)"
                class="dropdown-item"
              >
                {{ category.name }}
              </a>
            </div>
          </div>
          
          <router-link to="/favorites" class="nav-link">
            내가 찜한 리스트
          </router-link>
        </div>
      </div>
      
      <div class="header-right">
        <div class="user-menu" @click="toggleUserDropdown">
          <span class="username">{{ displayName }}님</span>
          <span class="arrow" :class="{ 'open': showUserDropdown }">▼</span>
          
          <div v-if="showUserDropdown" class="dropdown-menu right">
            <button @click="handleLogout" class="dropdown-item">
              로그아웃
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 메인 컨텐츠 -->
    <main class="main-content">
      <!-- 로딩 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>영화 목록을 불러오는 중... ({{ loadingProgress }})</p>
      </div>

      <!-- 에러 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="loadMovies" class="retry-btn">다시 시도</button>
      </div>

      <!-- 영화 목록 -->
      <div v-else class="movies-container">
        <!-- 인기 영화 -->
        <MovieRow
          v-if="popularMovies.length"
          title="인기 영화"
          :movies="popularMovies"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />

        <!-- 액션 -->
        <MovieRow
          v-if="actionMovies.length"
          title="액션"
          :movies="actionMovies"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />

        <!-- 코미디 -->
        <MovieRow
          v-if="comedyMovies.length"
          title="코미디"
          :movies="comedyMovies"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />

        <!-- 로맨스 -->
        <MovieRow
          v-if="romanceMovies.length"
          title="로맨스"
          :movies="romanceMovies"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />

        <!-- 스릴러 -->
        <MovieRow
          v-if="thrillerMovies.length"
          title="스릴러"
          :movies="thrillerMovies"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />

        <!-- 판타지 -->
        <MovieRow
          v-if="fantasyMovies.length"
          title="판타지"
          :movies="fantasyMovies"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />

        <!-- SF -->
        <MovieRow
          v-if="sfMovies.length"
          title="SF"
          :movies="sfMovies"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />

        <!-- 애니메이션 -->
        <MovieRow
          v-if="animationMovies.length"
          title="애니메이션"
          :movies="animationMovies"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { movieAPI } from '@/api/movies'
import MovieRow from '@/components/MovieRow.vue'

export default {
  name: 'MovieListView',
  components: {
    MovieRow
  },
  setup() {
    const authStore = useAuthStore()
    
    // 사용자 정보 computed
    const user = computed(() => authStore.user)
    const displayName = computed(() => {
      if (!user.value) return '사용자'
      return user.value.nickname || user.value.username || '사용자'
    })

    const loading = ref(true)
    const loadingProgress = ref('')
    const error = ref(null)

    const showCategoryDropdown = ref(false)
    const showUserDropdown = ref(false)

    const categories = [
      { id: 'action', name: '액션' },
      { id: 'comedy', name: '코미디' },
      { id: 'romance', name: '로맨스' },
      { id: 'thriller', name: '스릴러' },
      { id: 'fantasy', name: '판타지' },
      { id: 'sf', name: 'SF' },
      { id: 'animation', name: '애니메이션' }
    ]

    const popularMovies = ref([])
    const actionMovies = ref([])
    const comedyMovies = ref([])
    const romanceMovies = ref([])
    const thrillerMovies = ref([])
    const fantasyMovies = ref([])
    const sfMovies = ref([])
    const animationMovies = ref([])

    const toggleCategoryDropdown = () => {
      showCategoryDropdown.value = !showCategoryDropdown.value
      showUserDropdown.value = false
    }

    const toggleUserDropdown = () => {
      showUserDropdown.value = !showUserDropdown.value
      showCategoryDropdown.value = false
    }

    const selectCategory = (category) => {
      showCategoryDropdown.value = false
      const element = document.querySelector(`[title="${category.name}"]`)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }

    const handleLogout = async () => {
      await authStore.logout()
    }

    const loadMovies = async () => {
      loading.value = true
      loadingProgress.value = '인기 영화 로딩 중...'
      error.value = null

      try {
        // 순차적으로 로딩 (동시 요청 방지!)
        
        // 1. 인기 영화
        loadingProgress.value = '인기 영화 로딩 중... (1/8)'
        const popularRes = await movieAPI.getPopularMovies()
        popularMovies.value = popularRes.data.results

        // 2. 액션
        loadingProgress.value = '액션 영화 로딩 중... (2/8)'
        await new Promise(resolve => setTimeout(resolve, 300))
        const actionRes = await movieAPI.getMoviesByGenre('action')
        actionMovies.value = actionRes.data.results

        // 3. 코미디
        loadingProgress.value = '코미디 영화 로딩 중... (3/8)'
        await new Promise(resolve => setTimeout(resolve, 300))
        const comedyRes = await movieAPI.getMoviesByGenre('comedy')
        comedyMovies.value = comedyRes.data.results

        // 4. 로맨스
        loadingProgress.value = '로맨스 영화 로딩 중... (4/8)'
        await new Promise(resolve => setTimeout(resolve, 300))
        const romanceRes = await movieAPI.getMoviesByGenre('romance')
        romanceMovies.value = romanceRes.data.results

        // 5. 스릴러
        loadingProgress.value = '스릴러 영화 로딩 중... (5/8)'
        await new Promise(resolve => setTimeout(resolve, 300))
        const thrillerRes = await movieAPI.getMoviesByGenre('thriller')
        thrillerMovies.value = thrillerRes.data.results

        // 6. 판타지
        loadingProgress.value = '판타지 영화 로딩 중... (6/8)'
        await new Promise(resolve => setTimeout(resolve, 300))
        const fantasyRes = await movieAPI.getMoviesByGenre('fantasy')
        fantasyMovies.value = fantasyRes.data.results

        // 7. SF
        loadingProgress.value = 'SF 영화 로딩 중... (7/8)'
        await new Promise(resolve => setTimeout(resolve, 300))
        const sfRes = await movieAPI.getMoviesByGenre('sf')
        sfMovies.value = sfRes.data.results

        // 8. 애니메이션
        loadingProgress.value = '애니메이션 로딩 중... (8/8)'
        await new Promise(resolve => setTimeout(resolve, 300))
        const animationRes = await movieAPI.getMoviesByGenre('animation')
        animationMovies.value = animationRes.data.results

        loadingProgress.value = '완료!'

      } catch (err) {
        console.error('영화 목록 로드 실패:', err)
        error.value = '영화 목록을 불러오는데 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    const handleMovieClick = (movie) => {
      console.log('영화 클릭:', movie)
    }

    const handleFavoriteToggled = ({ movieId, isFavorited }) => {
      const updateMovie = (movies) => {
        const movie = movies.find(m => m.id === movieId)
        if (movie) {
          movie.is_favorited = isFavorited
        }
      }

      updateMovie(popularMovies.value)
      updateMovie(actionMovies.value)
      updateMovie(comedyMovies.value)
      updateMovie(romanceMovies.value)
      updateMovie(thrillerMovies.value)
      updateMovie(fantasyMovies.value)
      updateMovie(sfMovies.value)
      updateMovie(animationMovies.value)
    }

    onMounted(() => {
      // 디버깅: 사용자 정보 확인
      console.log('🔍 현재 사용자:', user.value)
      console.log('🔍 인증 상태:', authStore.isAuthenticated)
      
      loadMovies()
    })

    return {
      user,
      displayName,
      loading,
      loadingProgress,
      error,
      showCategoryDropdown,
      showUserDropdown,
      categories,
      popularMovies,
      actionMovies,
      comedyMovies,
      romanceMovies,
      thrillerMovies,
      fantasyMovies,
      sfMovies,
      animationMovies,
      toggleCategoryDropdown,
      toggleUserDropdown,
      selectCategory,
      handleLogout,
      loadMovies,
      handleMovieClick,
      handleFavoriteToggled
    }
  }
}
</script>

<style scoped>
.movie-list-view {
  min-height: 100vh;
  background: #141414;
}

/* 헤더 */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  background: linear-gradient(to bottom, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 50px;
  z-index: 100;
  transition: background 0.3s;
}

.header:hover {
  background: rgba(0, 0, 0, 0.95);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 30px;
}

.logo {
  font-size: 28px;
  font-weight: 900;
  color: #e50914;
  margin: 0;
  cursor: pointer;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: #e5e5e5;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #ffffff;
}

/* 드롭다운 */
.dropdown {
  position: relative;
}

.dropdown-btn {
  background: none;
  border: none;
  color: #e5e5e5;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: color 0.2s;
}

.dropdown-btn:hover {
  color: #ffffff;
}

.arrow {
  font-size: 10px;
  transition: transform 0.2s;
}

.arrow.open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 10px;
  background: rgba(0, 0, 0, 0.95);
  border: 1px solid #333;
  border-radius: 4px;
  min-width: 150px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.dropdown-menu.right {
  left: auto;
  right: 0;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 10px 16px;
  background: none;
  border: none;
  color: #e5e5e5;
  font-size: 14px;
  text-align: left;
  cursor: pointer;
  transition: background 0.2s;
  text-decoration: none;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* 유저 메뉴 */
.header-right {
  display: flex;
  align-items: center;
}

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #e5e5e5;
  font-size: 14px;
}

.username {
  font-weight: 500;
}

/* 메인 컨텐츠 */
.main-content {
  padding-top: 90px;
  padding-bottom: 50px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  color: #e5e5e5;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid #333;
  border-top-color: #e50914;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  color: #e5e5e5;
}

.retry-btn {
  margin-top: 20px;
  padding: 10px 24px;
  background: #e50914;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-btn:hover {
  background: #f40612;
}

.movies-container {
  padding: 0;
}

@media (max-width: 768px) {
  .header {
    padding: 0 20px;
    height: 60px;
  }
  
  .logo {
    font-size: 24px;
  }
  
  .nav-menu {
    gap: 15px;
  }
  
  .nav-link,
  .dropdown-btn {
    font-size: 13px;
  }
  
  .main-content {
    padding-top: 80px;
  }
}
</style>