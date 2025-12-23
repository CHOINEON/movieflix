// frontend/src/api/movies.js

import axios from './axios'

export const movieAPI = {
  // 인기 영화
  getPopularMovies(page = 1) {
    return axios.get('/movies/popular/', { params: { page } })
  },

  // 장르별 영화
  getMoviesByGenre(genre, page = 1) {
    return axios.get(`/movies/genre/${genre}/`, { params: { page } })
  },

  // 영화 상세 정보 (TMDB ID)
  getMovieDetail(tmdbId) {
    return axios.get(`/movies/detail/${tmdbId}/`)
  },

  // 찜하기 토글
  toggleFavorite(movieId) {
    return axios.post(`/movies/${movieId}/favorite/`)
  },

  // 내가 찜한 영화
  getMyFavorites() {
    return axios.get('/movies/favorites/')
  }
}