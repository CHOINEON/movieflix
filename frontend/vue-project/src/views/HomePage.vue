<template>
  <div class="home-page">
    <div class="background-overlay"></div>
    
    <div class="logo-section">
      <h1 class="logo">MOVIEFLIX</h1>
    </div>

    <div class="login-container">
      <h2 class="login-title">로그인</h2>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <input 
          v-model="loginForm.username"
          type="text" 
          class="input-field" 
          placeholder="이메일 또는 사용자 이름"
          required
        />
        
        <input 
          v-model="loginForm.password"
          type="password" 
          class="input-field" 
          placeholder="비밀번호"
          required
        />
        
        <button 
          type="submit" 
          class="login-button"
          :disabled="loading"
        >
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
        
        <div class="divider">
          <span>또는</span>
        </div>
        
        <router-link to="/signup" class="signup-button">
          회원가입
        </router-link>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'

export default {
  name: 'HomePage',
  setup() {
    const authStore = useAuthStore()
    
    const loginForm = ref({
      username: '',
      password: ''
    })
    
    const errorMessage = ref('')
    const loading = ref(false)

    const handleLogin = async () => {
      if (!loginForm.value.username || !loginForm.value.password) {
        errorMessage.value = '아이디와 비밀번호를 모두 입력해주세요.'
        return
      }

      loading.value = true
      errorMessage.value = ''

      try {
        await authStore.login({
          username: loginForm.value.username,
          password: loginForm.value.password
        })
      } catch (error) {
        errorMessage.value = error.response?.data?.error || '로그인에 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    return {
      loginForm,
      errorMessage,
      loading,
      handleLogin
    }
  }
}
</script>

<style scoped>
.home-page {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9)),
              url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1920&h=1080&fit=crop') center/cover;
  overflow: hidden;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.logo-section {
  position: absolute;
  top: 30px;
  left: 50px;
  z-index: 10;
}

.logo {
  font-size: 42px;
  font-weight: 900;
  color: #e50914;
  letter-spacing: 3px;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.login-container {
  position: relative;
  z-index: 10;
  background: rgba(0, 0, 0, 0.75);
  padding: 60px 68px 40px;
  border-radius: 4px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.login-title {
  color: #ffffff;
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 28px 0;
  text-align: left;
}

.error-message {
  background: #e87c03;
  color: #ffffff;
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 16px;
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-field {
  background: #333333;
  border: none;
  border-radius: 4px;
  color: #ffffff;
  padding: 16px 20px;
  font-size: 16px;
  outline: none;
  transition: background 0.2s;
}

.input-field::placeholder {
  color: #8c8c8c;
}

.input-field:focus {
  background: #454545;
}

.login-button {
  background: #e50914;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  padding: 16px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 24px;
  transition: background 0.2s;
}

.login-button:hover:not(:disabled) {
  background: #f40612;
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.divider {
  text-align: center;
  color: #8c8c8c;
  margin: 20px 0;
  position: relative;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 40%;
  height: 1px;
  background: #333333;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.signup-button {
  background: transparent;
  color: #ffffff;
  border: 1px solid #8c8c8c;
  border-radius: 4px;
  padding: 16px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  transition: all 0.2s;
  display: block;
}

.signup-button:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #ffffff;
}

@media (max-width: 768px) {
  .login-container {
    padding: 40px 30px;
    margin: 0 20px;
  }
  
  .logo {
    font-size: 32px;
    left: 20px;
  }
}
</style>