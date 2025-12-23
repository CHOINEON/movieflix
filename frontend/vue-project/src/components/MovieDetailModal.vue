<!-- frontend/src/components/MovieDetailModal.vue -->

<template>
  <Transition name="modal">
    <div v-if="show" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <!-- 닫기 버튼 -->
        <button class="close-btn" @click="closeModal">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>

        <!-- 로딩 -->
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
        </div>

        <!-- 에러 -->
        <div v-else-if="error" class="error">
          <p>{{ error }}</p>
          <button @click="closeModal" class="retry-btn">닫기</button>
        </div>

        <!-- 영화 상세 -->
        <div v-else-if="movie" class="modal-content">
          <!-- 상단: 배경 이미지 + 예고편 -->
          <div class="hero-section">
            <!-- 배경 이미지 -->
            <div 
              class="backdrop" 
              :style="{ backgroundImage: `url(${movie.backdrop_url})` }"
            >
              <div class="backdrop-overlay"></div>
            </div>

            <!-- 예고편 (있으면) -->
            <div v-if="movie.trailer" class="trailer-container">
              <iframe
                :src="movie.trailer.youtube_url + '?autoplay=1&mute=1&controls=1'"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
            </div>

            <!-- 영화 정보 오버레이 -->
            <div class="hero-info">
              <h1 class="movie-title">{{ movie.title }}</h1>
              <div class="movie-meta">
                <span class="rating">⭐ {{ movie.vote_average.toFixed(1) }}</span>
                <span class="year">{{ releaseYear }}</span>
                <span v-if="movie.runtime" class="runtime">{{ movie.runtime }}분</span>
              </div>
              
              <!-- 액션 버튼 -->
              <div class="action-buttons">
                <button class="play-btn">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                  재생
                </button>
                
                <button 
                  class="favorite-btn"
                  :class="{ 'favorited': movie.is_favorited }"
                  @click="handleToggleFavorite"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- 하단: 상세 정보 -->
          <div class="details-section">
            <div class="details-grid">
              <!-- 왼쪽: 줄거리 -->
              <div class="left-column">
                <h3 class="section-title">줄거리</h3>
                <p class="overview">{{ movie.overview || '줄거리 정보가 없습니다.' }}</p>
              </div>

              <!-- 오른쪽: 메타 정보 -->
              <div class="right-column">
                <!-- 출연진 -->
                <div class="info-item">
                  <span class="info-label">출연:</span>
                  <span class="info-value">{{ castNames }}</span>
                </div>

                <!-- 감독 -->
                <div v-if="directorNames" class="info-item">
                  <span class="info-label">감독:</span>
                  <span class="info-value">{{ directorNames }}</span>
                </div>

                <!-- 장르 -->
                <div class="info-item">
                  <span class="info-label">장르:</span>
                  <span class="info-value">{{ movie.genres.join(', ') }}</span>
                </div>

                <!-- 평점 -->
                <div class="info-item">
                  <span class="info-label">평점:</span>
                  <span class="info-value">⭐ {{ movie.vote_average.toFixed(1) }} ({{ movie.vote_count.toLocaleString() }}명)</span>
                </div>
              </div>
            </div>

            <!-- 출연진 목록 -->
            <div v-if="movie.cast && movie.cast.length" class="cast-section">
              <h3 class="section-title">출연진</h3>
              <div class="cast-grid">
                <div 
                  v-for="actor in movie.cast.slice(0, 6)" 
                  :key="actor.name"
                  class="cast-card"
                >
                  <div 
                    class="cast-image"
                    :style="{ 
                      backgroundImage: actor.profile_path ? `url(${actor.profile_path})` : 'none',
                      backgroundColor: actor.profile_path ? 'transparent' : '#333'
                    }"
                  >
                    <div v-if="!actor.profile_path" class="no-image">
                      <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                      </svg>
                    </div>
                  </div>
                  <div class="cast-info">
                    <div class="cast-name">{{ actor.name }}</div>
                    <div class="cast-character">{{ actor.character }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { movieAPI } from '@/api/movies'

export default {
  name: 'MovieDetailModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    tmdbId: {
      type: Number,
      default: null
    }
  },
  emits: ['close', 'favorite-toggled'],
  setup(props, { emit }) {
    const movie = ref(null)
    const loading = ref(false)
    const error = ref(null)

    const releaseYear = computed(() => {
      if (!movie.value?.release_date) return ''
      return new Date(movie.value.release_date).getFullYear()
    })

    const castNames = computed(() => {
      if (!movie.value?.cast || movie.value.cast.length === 0) return '정보 없음'
      return movie.value.cast.slice(0, 3).map(actor => actor.name).join(', ')
    })

    const directorNames = computed(() => {
      if (!movie.value?.directors || movie.value.directors.length === 0) return null
      return movie.value.directors.map(d => d.name).join(', ')
    })

    const loadMovieDetail = async () => {
      if (!props.tmdbId) return

      loading.value = true
      error.value = null

      try {
        console.log('🎬 영화 상세 정보 로딩:', props.tmdbId)
        const response = await movieAPI.getMovieDetail(props.tmdbId)
        movie.value = response.data
        console.log('✅ 영화 상세 정보:', movie.value)
      } catch (err) {
        console.error('❌ 영화 상세 정보 로드 실패:', err)
        error.value = '영화 정보를 불러오는데 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    const closeModal = () => {
      emit('close')
      movie.value = null
    }

    const handleToggleFavorite = async () => {
      if (!movie.value) return

      try {
        console.log('❤️ 찜하기 토글:', movie.value.id)
        await movieAPI.toggleFavorite(movie.value.id)
        
        // 상태 토글
        movie.value.is_favorited = !movie.value.is_favorited
        
        // 부모에게 알림
        emit('favorite-toggled', {
          movieId: movie.value.id,
          isFavorited: movie.value.is_favorited
        })
      } catch (err) {
        console.error('❌ 찜하기 실패:', err)
      }
    }

    // tmdbId가 변경될 때마다 영화 정보 로드
    watch(() => props.tmdbId, (newId) => {
      if (newId && props.show) {
        loadMovieDetail()
      }
    }, { immediate: true })

    // show가 true가 될 때 영화 정보 로드
    watch(() => props.show, (newShow) => {
      if (newShow && props.tmdbId) {
        loadMovieDetail()
      }
    })

    return {
      movie,
      loading,
      error,
      releaseYear,
      castNames,
      directorNames,
      closeModal,
      handleToggleFavorite
    }
  }
}
</script>

<style scoped>
/* 모달 트랜지션 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}

/* 오버레이 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 40px;
  overflow-y: auto;
}

/* 모달 컨테이너 */
.modal-container {
  background: #181818;
  border-radius: 12px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.7);
}

/* 닫기 버튼 */
.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  background: rgba(0, 0, 0, 0.7);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.9);
}

/* 로딩 */
.loading {
  padding: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid #333;
  border-top-color: #e50914;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 에러 */
.error {
  padding: 100px 40px;
  text-align: center;
  color: #e5e5e5;
}

.retry-btn {
  margin-top: 20px;
  padding: 10px 24px;
  background: #e50914;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
}

/* 히어로 섹션 */
.hero-section {
  position: relative;
  width: 100%;
  height: 500px;
  overflow: hidden;
  border-radius: 12px 12px 0 0;
}

.backdrop {
  position: absolute;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
}

.backdrop-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(to top, #181818, transparent);
}

/* 예고편 */
.trailer-container {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.trailer-container iframe {
  width: 100%;
  height: 100%;
}

/* 히어로 정보 */
.hero-info {
  position: absolute;
  bottom: 40px;
  left: 40px;
  right: 40px;
  z-index: 2;
}

.movie-title {
  font-size: 42px;
  font-weight: 700;
  color: white;
  margin: 0 0 12px 0;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
}

.movie-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  font-size: 16px;
  color: #e5e5e5;
}

.movie-meta span {
  display: flex;
  align-items: center;
}

/* 액션 버튼 */
.action-buttons {
  display: flex;
  gap: 12px;
}

.play-btn,
.favorite-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.play-btn {
  background: white;
  color: black;
}

.play-btn:hover {
  background: rgba(255, 255, 255, 0.9);
}

.favorite-btn {
  background: rgba(42, 42, 42, 0.6);
  color: white;
  padding: 12px;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.favorite-btn:hover {
  background: rgba(42, 42, 42, 0.8);
  border-color: white;
}

.favorite-btn.favorited {
  background: rgba(229, 9, 20, 0.2);
  border-color: #e50914;
}

.favorite-btn.favorited svg {
  fill: #e50914;
}

/* 상세 섹션 */
.details-section {
  padding: 40px;
}

.details-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin: 0 0 16px 0;
}

.overview {
  font-size: 16px;
  line-height: 1.6;
  color: #e5e5e5;
  margin: 0;
}

/* 메타 정보 */
.right-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 14px;
  color: #777;
  font-weight: 600;
}

.info-value {
  font-size: 14px;
  color: #e5e5e5;
}

/* 출연진 그리드 */
.cast-section {
  margin-top: 40px;
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}

.cast-card {
  display: flex;
  flex-direction: column;
}

.cast-image {
  width: 100%;
  aspect-ratio: 2/3;
  background-size: cover;
  background-position: center;
  border-radius: 8px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.no-image {
  color: #777;
}

.cast-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.cast-name {
  font-size: 14px;
  font-weight: 600;
  color: #e5e5e5;
}

.cast-character {
  font-size: 13px;
  color: #777;
}

/* 스크롤바 */
.modal-container::-webkit-scrollbar {
  width: 8px;
}

.modal-container::-webkit-scrollbar-track {
  background: #181818;
}

.modal-container::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: #777;
}

/* 반응형 */
@media (max-width: 768px) {
  .modal-overlay {
    padding: 0;
  }

  .modal-container {
    max-height: 100vh;
    border-radius: 0;
  }

  .hero-section {
    height: 300px;
  }

  .movie-title {
    font-size: 28px;
  }

  .details-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .cast-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
}
</style>