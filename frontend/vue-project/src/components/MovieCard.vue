<!-- frontend/src/components/MovieCard.vue -->

<template>
  <div class="movie-card" @click="handleClick">
    <div class="poster-container">
      <img 
        v-if="movie.poster_url" 
        :src="movie.poster_url" 
        :alt="movie.title"
        class="poster"
      />
      <div v-else class="no-poster">
        <span>{{ movie.title }}</span>
      </div>
      
      <!-- 찜하기 버튼 -->
      <button 
        v-if="showFavoriteButton"
        class="favorite-btn"
        @click.stop="handleFavorite"
        :class="{ 'favorited': movie.is_favorited }"
      >
        {{ movie.is_favorited ? '❤️' : '🤍' }}
      </button>
      
      <!-- 평점 -->
      <div class="rating">
        <span class="star">⭐</span>
        <span>{{ movie.vote_average.toFixed(1) }}</span>
      </div>
    </div>
    
    <div class="info">
      <h3 class="title">{{ movie.title }}</h3>
      <p class="release-date" v-if="movie.release_date">
        {{ formatDate(movie.release_date) }}
      </p>
    </div>
  </div>
</template>

<script>
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
      default: true
    }
  },
  setup(props, { emit }) {
    const authStore = useAuthStore()

    const handleClick = () => {
      emit('click', props.movie)
    }

    const handleFavorite = async () => {
      if (!authStore.isAuthenticated) {
        alert('로그인이 필요합니다.')
        return
      }

      try {
        const response = await movieAPI.toggleFavorite(props.movie.id)
        emit('favorite-toggled', {
          movieId: props.movie.id,
          isFavorited: response.data.is_favorited
        })
      } catch (error) {
        console.error('찜하기 실패:', error)
        alert('찜하기에 실패했습니다.')
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.getFullYear() + '년'
    }

    return {
      handleClick,
      handleFavorite,
      formatDate
    }
  }
}
</script>

<style scoped>
.movie-card {
  cursor: pointer;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.movie-card:hover {
  transform: scale(1.05);
  z-index: 10;
}

.poster-container {
  position: relative;
  width: 100%;
  aspect-ratio: 2/3;
  border-radius: 4px;
  overflow: hidden;
  background: #2a2a2a;
}

.poster {
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 10px;
  text-align: center;
  font-weight: 600;
}

.favorite-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.7);
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 5;
}

.favorite-btn:hover {
  transform: scale(1.1);
  background: rgba(0, 0, 0, 0.9);
}

.favorite-btn.favorited {
  animation: heartbeat 0.3s ease;
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.rating {
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
  color: white;
}

.star {
  font-size: 16px;
}

.info {
  padding: 8px 4px;
}

.title {
  font-size: 14px;
  font-weight: 600;
  color: #e5e5e5;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
  min-height: 2.6em;
}

.release-date {
  font-size: 12px;
  color: #999;
  margin: 0;
}
</style>