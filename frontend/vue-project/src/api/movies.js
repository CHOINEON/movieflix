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
  },

  // ==================== 리뷰 API ====================

  // 영화 리뷰 목록 조회
  getMovieReviews(movieId) {
    return axios.get(`/movies/${movieId}/reviews/`)
  },

  // 리뷰 작성
  createReview(movieId, reviewData) {
    return axios.post(`/movies/${movieId}/reviews/`, reviewData)
  },

  // 리뷰 수정
  updateReview(reviewId, reviewData) {
    return axios.put(`/movies/reviews/${reviewId}/`, reviewData)
  },

  // 리뷰 삭제
  deleteReview(reviewId) {
    return axios.delete(`/movies/reviews/${reviewId}/`)
  },

  // 리뷰 좋아요 토글
  toggleReviewLike(reviewId) {
    return axios.post(`/movies/reviews/${reviewId}/like/`)
  }
}