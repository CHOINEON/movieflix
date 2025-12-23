<!-- frontend/src/components/MovieRow.vue -->

<template>
  <div class="movie-row">
    <h2 class="row-title" :title="title">{{ title }}</h2>
    
    <div class="movies-slider">
      <button 
        class="slider-btn prev" 
        @click="scrollLeft"
        v-show="canScrollLeft"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
          <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
        </svg>
      </button>

      <div class="movies-container" ref="container" @scroll="updateScrollState">
        <MovieCard
          v-for="movie in movies"
          :key="movie.id"
          :movie="movie"
          @movie-click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />
      </div>

      <button 
        class="slider-btn next" 
        @click="scrollRight"
        v-show="canScrollRight"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
          <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import MovieCard from './MovieCard.vue'

export default {
  name: 'MovieRow',
  components: {
    MovieCard
  },
  props: {
    title: {
      type: String,
      required: true
    },
    movies: {
      type: Array,
      required: true
    }
  },
  emits: ['movie-click', 'favorite-toggled'],
  setup(props, { emit }) {
    const container = ref(null)
    const canScrollLeft = ref(false)
    const canScrollRight = ref(false)

    const updateScrollState = () => {
      if (!container.value) return
      
      const { scrollLeft, scrollWidth, clientWidth } = container.value
      canScrollLeft.value = scrollLeft > 0
      canScrollRight.value = scrollLeft < scrollWidth - clientWidth - 10
    }

    const scrollLeft = () => {
      if (container.value) {
        container.value.scrollBy({ left: -800, behavior: 'smooth' })
      }
    }

    const scrollRight = () => {
      if (container.value) {
        container.value.scrollBy({ left: 800, behavior: 'smooth' })
      }
    }

    const handleMovieClick = (movie) => {
      console.log('📺 MovieRow에서 영화 클릭:', movie)
      emit('movie-click', movie)
    }

    const handleFavoriteToggled = (data) => {
      console.log('❤️ MovieRow에서 찜하기:', data)
      emit('favorite-toggled', data)
    }

    onMounted(() => {
      updateScrollState()
      
      if (container.value) {
        container.value.addEventListener('scroll', updateScrollState)
      }
    })

    return {
      container,
      canScrollLeft,
      canScrollRight,
      scrollLeft,
      scrollRight,
      updateScrollState,
      handleMovieClick,
      handleFavoriteToggled
    }
  }
}
</script>

<style scoped>
.movie-row {
  margin-bottom: 40px;
  position: relative;
  padding: 0 50px;
}

.row-title {
  font-size: 20px;
  font-weight: 700;
  color: #e5e5e5;
  margin: 0 0 16px 0;
  padding-left: 4px;
}

.movies-slider {
  position: relative;
}

.movies-container {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  padding: 4px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.movies-container::-webkit-scrollbar {
  display: none;
}

.movies-container > * {
  flex: 0 0 auto;
  width: 200px;
}

/* 슬라이더 버튼 */
.slider-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.slider-btn:hover {
  background: rgba(0, 0, 0, 0.8);
}

.slider-btn.prev {
  left: 0;
}

.slider-btn.next {
  right: 0;
}

@media (max-width: 768px) {
  .movie-row {
    padding: 0 20px;
  }

  .movies-container > * {
    width: 150px;
  }

  .slider-btn {
    display: none;
  }
}
</style>