<!-- frontend/src/views/FavoritesView.vue -->

<template>
  <div class="favorites-view">
    <!-- 상단 네비게이션 -->
    <header class="header">
      <div class="header-left">
        <h1 class="logo" @click="$router.push('/movies')">MOVIEFLIX</h1>
        
        <div class="nav-menu">
          <router-link to="/movies" class="nav-link">
            홈
          </router-link>
          <router-link to="/favorites" class="nav-link active">
            내가 찜한 리스트
          </router-link>
          <router-link to="/chatbot" class="nav-link">
            Claude가 말아주는 영화추천
          </router-link>
        </div>
      </div>
      
      <div class="header-right">
        <div class="user-menu" @click="toggleUserDropdown">
          <span class="username">{{ user?.nickname || user?.username }}님</span>
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
      <h1 class="page-title">내가 찜한 리스트</h1>

      <!-- 로딩 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>찜한 영화를 불러오는 중...</p>
      </div>

      <!-- 에러 -->
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="loadFavorites" class="retry-btn">다시 시도</button>
      </div>

      <!-- 찜한 영화 없음 -->
      <div v-else-if="favorites.length === 0" class="empty">
        <p class="empty-icon">💔</p>
        <h2>찜한 영화가 없습니다</h2>
        <p>마음에 드는 영화에 하트를 눌러보세요!</p>
        <button @click="$router.push('/movies')" class="browse-btn">
          영화 둘러보기
        </button>
      </div>

      <!-- 찜한 영화 목록 -->
      <div v-else class="favorites-grid">
        <MovieCard
          v-for="favorite in favorites"
          :key="favorite.id"
          :movie="favorite.movie"
          :show-favorite-button="false"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />
      </div>
    </main>

    <!-- 영화 상세 모달 -->
    <MovieDetailModal
      :show="showDetailModal"
      :tmdb-id="selectedMovieTmdbId"
      @close="closeDetailModal"
      @favorite-toggled="handleFavoriteToggled"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { movieAPI } from '@/api/movies'
import MovieCard from '@/components/MovieCard.vue'
import MovieDetailModal from '@/components/MovieDetailModal.vue'

export default {
  name: 'FavoritesView',
  components: {
    MovieCard,
    MovieDetailModal
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const user = computed(() => authStore.user)

    const loading = ref(true)
    const error = ref(null)
    const showUserDropdown = ref(false)
    const favorites = ref([])

    // 모달 관련 ref
    const showDetailModal = ref(false)
    const selectedMovieTmdbId = ref(null)

    const toggleUserDropdown = () => {
      showUserDropdown.value = !showUserDropdown.value
    }

    const handleLogout = async () => {
      await authStore.logout()
    }

    const loadFavorites = async () => {
      loading.value = true
      error.value = null

      try {
        const response = await movieAPI.getMyFavorites()
        favorites.value = response.data
        console.log('✅ 찜한 영화 목록:', favorites.value)
      } catch (err) {
        console.error('❌ 찜한 영화 로드 실패:', err)
        error.value = '찜한 영화를 불러오는데 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    const handleMovieClick = (movie) => {
      console.log('🎬 영화 클릭:', movie)
      selectedMovieTmdbId.value = movie.tmdb_id
      showDetailModal.value = true
    }

    const closeDetailModal = () => {
      showDetailModal.value = false
      selectedMovieTmdbId.value = null
    }

    const handleFavoriteToggled = ({ movieId, isFavorited }) => {
      console.log('❤️ 찜하기 토글:', { movieId, isFavorited })
      
      if (!isFavorited) {
        // 찜 취소된 경우 목록에서 제거
        favorites.value = favorites.value.filter(
          fav => fav.movie.id !== movieId
        )
        console.log('🗑️ 목록에서 제거됨:', movieId)
      }
    }

    onMounted(() => {
      loadFavorites()
    })

    return {
      user,
      loading,
      error,
      showUserDropdown,
      favorites,
      showDetailModal,
      selectedMovieTmdbId,
      toggleUserDropdown,
      handleLogout,
      loadFavorites,
      handleMovieClick,
      closeDetailModal,
      handleFavoriteToggled
    }
  }
}
</script>

<style scoped>
.favorites-view {
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
  background: rgba(0, 0, 0, 0.95);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 50px;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
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

.nav-link.active {
  color: #ffffff;
  font-weight: 700;
}

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
  right: 0;
  margin-top: 10px;
  background: rgba(0, 0, 0, 0.95);
  border: 1px solid #333;
  border-radius: 4px;
  min-width: 120px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  z-index: 1000;
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
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* 메인 컨텐츠 */
.main-content {
  padding-top: 100px;
  padding-bottom: 50px;
  padding-left: 50px;
  padding-right: 50px;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #e5e5e5;
  margin: 0 0 30px 0;
}

/* 로딩 */
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

/* 에러 */
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

/* 찜한 영화 없음 */
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  color: #e5e5e5;
  text-align: center;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.empty h2 {
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 10px 0;
}

.empty p {
  font-size: 16px;
  color: #999;
  margin: 0 0 30px 0;
}

.browse-btn {
  padding: 12px 32px;
  background: #e50914;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.browse-btn:hover {
  background: #f40612;
}

/* 찜한 영화 그리드 */
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .main-content {
    padding: 90px 20px 30px 20px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .favorites-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 15px;
  }
}
</style>