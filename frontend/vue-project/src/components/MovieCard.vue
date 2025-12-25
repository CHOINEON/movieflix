<!-- frontend/src/components/MovieCard.vue -->

<template>
  <div class="movie-card" @click="handleCardClick">
    <div class="movie-poster">
      <img 
        v-if="movie.poster_url" 
        :src="movie.poster_url" 
        :alt="movie.title"
      >
      <div v-else class="no-poster">
        <span>No Image</span>
      </div>
      
      <!-- 찜하기 버튼 (showFavoriteButton이 true일 때만 표시) -->
      <button 
        v-if="showFavoriteButton"
        class="favorite-btn"
        :class="{ 'favorited': movie.is_favorited }"
        @click.stop="handleToggleFavorite"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </button>

      <!-- 평점 배지 -->
      <div class="rating-badge">
        <span class="star">⭐</span>
        <span class="score">{{ movie.vote_average.toFixed(1) }}</span>
      </div>
    </div>

    <div class="movie-info">
      <h3 class="movie-title">{{ movie.title }}</h3>
      <p class="movie-year">{{ releaseYear }}</p>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { movieAPI } from '@/api/movies'

export default {
  name: 'MovieCard',
  props: {
    movie: {
      type: Object,
      required: true
    },
    showFavoriteButton: {
      type: Boolean,
      default: true  // 기본값은 true (하트 버튼 표시)
    }
  },
  emits: ['movie-click', 'favorite-toggled'],
  setup(props, { emit }) {
    const authStore = useAuthStore()

    const releaseYear = computed(() => {
      if (!props.movie.release_date) return ''
      return new Date(props.movie.release_date).getFullYear()
    })

    const handleCardClick = () => {
      console.log('🎬 카드 클릭:', props.movie)
      emit('movie-click', props.movie)
    }

    const handleToggleFavorite = async () => {
      // 로그인 확인
      if (!authStore.isAuthenticated) {
        alert('로그인이 필요합니다.')
        return
      }

      try {
        console.log('❤️ 찜하기 토글:', props.movie.id, props.movie.title)
        
        // API 호출
        const response = await movieAPI.toggleFavorite(props.movie.id)
        
        console.log('✅ 찜하기 응답:', response.data)
        
        // 부모 컴포넌트에 이벤트 전달
        emit('favorite-toggled', {
          movieId: props.movie.id,
          isFavorited: response.data.is_favorited
        })
        
      } catch (err) {
        console.error('❌ 찜하기 실패:', err)
        alert('찜하기에 실패했습니다.')
      }
    }

    return {
      releaseYear,
      handleCardClick,
      handleToggleFavorite,
    }
  }
}
</script>

<style scoped>
.movie-card {
  cursor: pointer;
  transition: transform 0.3s ease;
  position: relative;
}

.movie-card:hover {
  transform: scale(1.05);
  z-index: 10;
}

.movie-poster {
  position: relative;
  width: 100%;
  aspect-ratio: 2/3;
  border-radius: 8px;
  overflow: hidden;
  background: #2a2a2a;
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-poster {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 14px;
}

/* 찜하기 버튼 */
.favorite-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 36px;
  height: 36px;
  background: rgba(0, 0, 0, 0.7);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: all 0.3s;
  z-index: 2;
}

.movie-card:hover .favorite-btn {
  opacity: 1;
}

.favorite-btn.favorited {
  opacity: 1;
}

.favorite-btn svg {
  color: white;
}

.favorite-btn.favorited svg {
  fill: #e50914;
  color: #e50914;
}

.favorite-btn:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: scale(1.1);
}

/* 평점 배지 */
.rating-badge {
  position: absolute;
  bottom: 8px;
  left: 8px;
  background: rgba(0, 0, 0, 0.8);
  padding: 4px 8px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 600;
}

.star {
  font-size: 12px;
}

.score {
  color: #ffd700;
}

/* 영화 정보 */
.movie-info {
  padding: 12px 4px;
}

.movie-title {
  font-size: 14px;
  font-weight: 600;
  color: #e5e5e5;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.movie-year {
  font-size: 13px;
  color: #808080;
  margin: 0;
}
</style>