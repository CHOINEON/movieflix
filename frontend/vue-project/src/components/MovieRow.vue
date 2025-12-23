<!-- frontend/src/components/MovieRow.vue -->

<template>
  <div class="movie-row">
    <h2 class="row-title">{{ title }}</h2>
    
    <div class="row-container">
      <button 
        v-if="showLeftArrow"
        class="scroll-btn left"
        @click="scrollLeft"
      >
        ‹
      </button>
      
      <div 
        class="movies-list" 
        ref="moviesListRef"
        @scroll="handleScroll"
      >
        <MovieCard
          v-for="movie in movies"
          :key="movie.id"
          :movie="movie"
          @click="handleMovieClick"
          @favorite-toggled="handleFavoriteToggled"
        />
      </div>
      
      <button 
        v-if="showRightArrow"
        class="scroll-btn right"
        @click="scrollRight"
      >
        ›
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
      default: () => []
    }
  },
  emits: ['movie-click', 'favorite-toggled'],
  setup(props, { emit }) {
    const moviesListRef = ref(null)
    const showLeftArrow = ref(false)
    const showRightArrow = ref(true)

    const handleScroll = () => {
      if (!moviesListRef.value) return
      
      const { scrollLeft, scrollWidth, clientWidth } = moviesListRef.value
      showLeftArrow.value = scrollLeft > 0
      showRightArrow.value = scrollLeft < scrollWidth - clientWidth - 10
    }

    const scrollLeft = () => {
      if (!moviesListRef.value) return
      moviesListRef.value.scrollBy({
        left: -moviesListRef.value.clientWidth,
        behavior: 'smooth'
      })
    }

    const scrollRight = () => {
      if (!moviesListRef.value) return
      moviesListRef.value.scrollBy({
        left: moviesListRef.value.clientWidth,
        behavior: 'smooth'
      })
    }

    const handleMovieClick = (movie) => {
      emit('movie-click', movie)
    }

    const handleFavoriteToggled = (data) => {
      emit('favorite-toggled', data)
    }

    onMounted(() => {
      handleScroll()
    })

    return {
      moviesListRef,
      showLeftArrow,
      showRightArrow,
      handleScroll,
      scrollLeft,
      scrollRight,
      handleMovieClick,
      handleFavoriteToggled
    }
  }
}
</script>

<style scoped>
.movie-row {
  margin-bottom: 40px;
}

.row-title {
  font-size: 20px;
  font-weight: 700;
  color: #e5e5e5;
  margin: 0 0 16px 50px;
}

.row-container {
  position: relative;
  padding: 0 50px;
}

.movies-list {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  padding: 4px 0;
  
  /* 스크롤바 숨기기 */
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.movies-list::-webkit-scrollbar {
  display: none;
}

.movies-list > * {
  width: 200px;
  flex-shrink: 0;
}

.scroll-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  border: none;
  color: white;
  font-size: 40px;
  cursor: pointer;
  z-index: 10;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scroll-btn:hover {
  background: rgba(0, 0, 0, 0.9);
}

.scroll-btn.left {
  left: 0;
}

.scroll-btn.right {
  right: 0;
}

@media (max-width: 768px) {
  .row-title {
    margin-left: 20px;
    font-size: 18px;
  }
  
  .row-container {
    padding: 0 20px;
  }
  
  .scroll-btn {
    display: none;
  }
  
  .movies-list > * {
    width: 150px;
  }
}
</style>