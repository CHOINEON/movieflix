// frontend/src/api/axios.js

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const instance = axios.create({
  baseURL: `${API_BASE_URL}/api`,  // 환경변수 사용
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})


// CSRF 토큰 가져오기 함수
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// 요청 인터셉터: 모든 요청에 CSRF 토큰 추가
instance.interceptors.request.use(
  (config) => {
    // POST, PUT, DELETE 요청에만 CSRF 토큰 추가
    if (['post', 'put', 'delete', 'patch'].includes(config.method.toLowerCase())) {
      const csrfToken = getCookie('csrftoken')
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
        console.log('✅ CSRF Token added:', csrfToken)
      } else {
        console.warn('⚠️ CSRF Token not found in cookies!')
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 응답 인터셉터: 에러 로깅
instance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 403) {
      console.error('❌ 403 Forbidden Error')
      console.error('Current cookies:', document.cookie)
      console.error('Request headers:', error.config.headers)
    }
    return Promise.reject(error)
  }
)

export default instance