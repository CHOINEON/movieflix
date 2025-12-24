// frontend/src/stores/chatStore.js
import { defineStore } from 'pinia'
import axios from '@/api/axios'  // ✅ 설정된 axios 인스턴스 사용

export const useChatStore = defineStore('chat', {
  state: () => ({
    /**
     * 채팅 메시지 배열
     * @type {Array<{role: 'user'|'assistant', content: string, timestamp: Date}>}
     */
    messages: [],
    
    /**
     * API 요청 로딩 상태
     * @type {boolean}
     */
    isLoading: false,
    
    /**
     * 에러 메시지
     * @type {string|null}
     */
    error: null
  }),

  actions: {
    /**
     * AI에게 메시지 전송
     * @param {string} message - 사용자 메시지
     */
    async sendMessage(message) {
      console.log('🚀 [chatStore] sendMessage 호출')
      console.log('📝 [chatStore] 메시지:', message)
      console.log('🍪 [chatStore] 쿠키:', document.cookie)
      
      // 사용자 메시지 추가
      this.messages.push({
        role: 'user',
        content: message,
        timestamp: new Date()
      })
      
      this.isLoading = true
      this.error = null
      
      try {
        console.log('🌐 [chatStore] API 요청 시작')
        
        // ✅ baseURL이 /api이므로 /movies/ai-chat/만 사용
        const response = await axios.post('/movies/ai-chat/', { message })
        
        console.log('✅ [chatStore] 응답 성공:', response.data)
        
        // AI 응답 추가
        this.messages.push({
          role: 'assistant',
          content: response.data.response,
          timestamp: new Date()
        })
        
      } catch (err) {
        console.error('❌ [chatStore] 요청 실패')
        console.error('상태:', err.response?.status)
        console.error('데이터:', err.response?.data)
        
        // 에러 처리
        if (err.response?.status === 401) {
          this.error = '로그인이 필요합니다.'
        } else if (err.response?.status === 403) {
          this.error = '인증 오류가 발생했습니다.'
        } else if (err.response?.data?.error) {
          this.error = err.response.data.error
        } else {
          this.error = 'AI 서비스에 연결할 수 없습니다.'
        }
        
      } finally {
        this.isLoading = false
      }
    },

    /**
     * 채팅 내역 초기화
     */
    clearMessages() {
      this.messages = []
      this.error = null
    }
  }
})