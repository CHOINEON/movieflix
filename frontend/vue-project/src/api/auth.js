// frontend/src/api/auth.js

import axios from './axios'

export const authAPI = {
  // 로그인
  async login(credentials) {
    try {
      // 1. CSRF 토큰 확보 (중요!)
      console.log('🔐 CSRF 토큰 요청 중...')
      await axios.get('/accounts/csrf/')
      console.log('✅ CSRF 토큰 요청 완료')
      console.log('📋 현재 쿠키:', document.cookie)
      
      // 2. 로그인 요청
      console.log('🔑 로그인 요청 중...')
      const response = await axios.post('/accounts/login/', credentials)
      console.log('✅ 로그인 성공')
      
      return response
    } catch (error) {
      console.error('❌ 로그인 에러:', error)
      throw error
    }
  },

  // 회원가입
  async signup(userData) {
    try {
      // 1. CSRF 토큰 확보
      console.log('🔐 CSRF 토큰 요청 중...')
      await axios.get('/accounts/csrf/')
      console.log('✅ CSRF 토큰 요청 완료')
      
      // 2. 회원가입 요청
      console.log('📝 회원가입 요청 중...')
      const response = await axios.post('/accounts/signup/', userData)
      console.log('✅ 회원가입 성공')
      
      return response
    } catch (error) {
      console.error('❌ 회원가입 에러:', error)
      throw error
    }
  },

  // 로그아웃
  async logout() {
    return axios.post('/accounts/logout/')
  },

  // 사용자 정보
  getUserInfo() {
    return axios.get('/accounts/user/')
  },

  // 프로필 업데이트
  updateProfile(data) {
    return axios.put('/accounts/profile/', data)
  },

  // 회원 탈퇴
  deleteAccount() {
    return axios.delete('/accounts/delete/')
  }
}