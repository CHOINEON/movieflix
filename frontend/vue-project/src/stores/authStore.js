// frontend/src/stores/authStore.js

import { defineStore } from 'pinia'
import { authAPI } from '@/api/auth'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),

  actions: {
    async login(credentials) {
      try {
        console.log('🔑 로그인 시도:', credentials.username)
        const response = await authAPI.login(credentials)
        
        // 사용자 정보 저장
        this.user = response.data
        this.isAuthenticated = true
        
        console.log('✅ 로그인 성공!')
        console.log('👤 사용자 정보:', this.user)
        console.log('🔐 인증 상태:', this.isAuthenticated)
        
        // 영화 목록 페이지로 이동
        router.push('/movies')
      } catch (error) {
        console.error('❌ 로그인 실패:', error)
        this.user = null
        this.isAuthenticated = false
        throw error
      }
    },

    async signup(userData) {
      try {
        console.log('📝 회원가입 시도:', userData.username)
        const response = await authAPI.signup(userData)
        
        // 사용자 정보 저장
        this.user = response.data
        this.isAuthenticated = true
        
        console.log('✅ 회원가입 성공!')
        console.log('👤 사용자 정보:', this.user)
        
        // 영화 목록 페이지로 이동
        router.push('/movies')
      } catch (error) {
        console.error('❌ 회원가입 실패:', error)
        this.user = null
        this.isAuthenticated = false
        throw error
      }
    },

    async logout() {
      try {
        console.log('👋 로그아웃 시도')
        await authAPI.logout()
        
        this.user = null
        this.isAuthenticated = false
        
        console.log('✅ 로그아웃 성공!')
        
        // 홈 페이지로 이동
        router.push('/')
      } catch (error) {
        console.error('❌ 로그아웃 실패:', error)
        // 실패해도 로컬 상태는 초기화
        this.user = null
        this.isAuthenticated = false
        router.push('/')
      }
    },

    async checkAuth() {
      try {
        console.log('🔍 인증 상태 확인 중...')
        const response = await authAPI.getUserInfo()
        
        this.user = response.data
        this.isAuthenticated = true
        
        console.log('✅ 인증 유효!')
        console.log('👤 사용자 정보:', this.user)
      } catch (error) {
        console.error('❌ 인증 실패:', error)
        this.user = null
        this.isAuthenticated = false
      }
    }
  }
})