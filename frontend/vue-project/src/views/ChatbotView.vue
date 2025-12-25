<!-- frontend/src/views/ChatbotView.vue -->

<template>
  <div class="background">
  <div class="chatbot-container">
    <div class="chat-header">
      <h2>🎬 AI 영화 추천</h2>
      <button @click="clearChat" class="clear-btn">대화 초기화</button>
    </div>

    <div class="messages-container" ref="messagesContainer">
      <div
        v-for="(msg, index) in chatStore.messages"
        :key="index"
        :class="['message', msg.role]"
      >
        <div class="message-content">
          <p>{{ msg.content }}</p>
          <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
        </div>
      </div>

      <!-- 로딩 인디케이터 -->
      <div v-if="chatStore.isLoading" class="message assistant">
        <div class="message-content typing">
          <span></span><span></span><span></span>
        </div>
      </div>

      <!-- 에러 메시지 -->
      <div v-if="chatStore.error" class="error-message">
        {{ chatStore.error }}
      </div>
    </div>

    <div class="input-container">
      <input
        v-model="userInput"
        @keypress.enter="sendMessage"
        :disabled="chatStore.isLoading"
        placeholder="영화 추천을 요청해보세요... (예: 액션 영화 추천해줘)"
        class="chat-input"
      />
      <button
        @click="sendMessage"
        :disabled="!userInput.trim() || chatStore.isLoading"
        class="send-btn"
      >
        전송
      </button>
    </div>
  </div></div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { useChatStore } from '@/stores/chatStore'
import { useAuthStore } from '@/stores/authStore'

const chatStore = useChatStore()
const authStore = useAuthStore()

// 사용자 입력값
const userInput = ref('')
// 메시지 컨테이너 참조
const messagesContainer = ref(null)

/**
 * 메시지 전송
 */
const sendMessage = async () => {
  if (!userInput.value.trim()) return
  
  const message = userInput.value
  userInput.value = ''
  
  await chatStore.sendMessage(message)
  
  // 스크롤을 최하단으로
  await nextTick()
  scrollToBottom()
}

/**
 * 채팅 초기화
 */
const clearChat = () => {
  if (confirm('대화 내역을 모두 삭제하시겠습니까?')) {
    chatStore.clearMessages()
  }
}

/**
 * 시간 포맷팅
 * @param {Date} date - 날짜 객체
 * @returns {string} - 포맷된 시간 문자열
 */
const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * 스크롤을 최하단으로 이동
 */
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.background {
  background :rgba(0, 0, 0, 0.2);
}

.chatbot-container {
  max-width: 800px;
  margin: 2rem auto;
  height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  background: #181818;
  border-radius: 12px;
  overflow: hidden;
}

.chat-header {
  padding: 1.5rem;
  background: #E50914;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h2 {
  margin: 0;
  color: white;
  font-size: 1.5rem;
}

.clear-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: background 0.3s;
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  animation: slideIn 0.3s ease;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 1rem 1.25rem;
  border-radius: 18px;
  position: relative;
}

.message.user .message-content {
  background: #E50914;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
  background: #2a2a2a;
  color: #e5e5e5;
  border-bottom-left-radius: 4px;
}

.message-content p {
  margin: 0 0 0.5rem 0;
  line-height: 1.5;
  white-space: pre-wrap;
}

.timestamp {
  font-size: 0.75rem;
  opacity: 0.7;
}

/* 타이핑 인디케이터 */
.typing {
  display: flex;
  gap: 0.3rem;
  padding: 1rem;
}

.typing span {
  width: 8px;
  height: 8px;
  background: #666;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.error-message {
  padding: 1rem;
  background: rgba(229, 9, 20, 0.2);
  border: 1px solid #E50914;
  border-radius: 8px;
  color: #ff6b6b;
  text-align: center;
}

.input-container {
  padding: 1.5rem;
  background: #2a2a2a;
  display: flex;
  gap: 1rem;
  border-top: 1px solid #333;
}

.chat-input {
  flex: 1;
  padding: 0.875rem 1.25rem;
  background: #1a1a1a;
  border: 1px solid #444;
  border-radius: 24px;
  color: white;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.chat-input:focus {
  border-color: #E50914;
}

.chat-input::placeholder {
  color: #666;
}

.send-btn {
  padding: 0.875rem 2rem;
  background: #E50914;
  border: none;
  border-radius: 24px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.send-btn:hover:not(:disabled) {
  background: #f40612;
}

.send-btn:disabled {
  background: #666;
  cursor: not-allowed;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 스크롤바 스타일 */
.messages-container::-webkit-scrollbar {
  width: 8px;
}

.messages-container::-webkit-scrollbar-track {
  background: #1a1a1a;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 4px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>