<template>
  <div class="signup-page">
    <div class="background-overlay"></div>
    
    <div class="logo-section">
      <router-link to="/">
        <h1 class="logo">MOVIEFLIX</h1>
      </router-link>
    </div>

    <div class="signup-container">
      <h2 class="signup-title">회원가입</h2>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
      
      <form @submit.prevent="handleSignup" class="signup-form">
        <input 
          v-model="signupForm.username"
          type="text" 
          class="input-field" 
          placeholder="사용자 이름 (아이디)"
          required
          minlength="3"
        />
        
        <input 
          v-model="signupForm.email"
          type="email" 
          class="input-field" 
          placeholder="이메일"
          required
        />
        
        <input 
          v-model="signupForm.nickname"
          type="text" 
          class="input-field" 
          placeholder="닉네임"
          required
        />
        
        <input 
          v-model="signupForm.password"
          type="password" 
          class="input-field" 
          placeholder="비밀번호"
          required
          minlength="8"
        />
        
        <input 
          v-model="signupForm.password_confirmation"
          type="password" 
          class="input-field" 
          placeholder="비밀번호 확인"
          required
        />
        
        <button 
          type="submit" 
          class="signup-button"
          :disabled="loading"
        >
          {{ loading ? '가입 중...' : '회원가입' }}
        </button>
        
        <div class="divider">
          <span>이미 계정이 있으신가요?</span>
        </div>
        
        <router-link to="/" class="login-link">
          로그인하기
        </router-link>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'

export default {
  name: 'SignupPage',
  setup() {
    const authStore = useAuthStore()
    
    const signupForm = ref({
      username: '',
      email: '',
      nickname: '',
      password: '',
      password_confirmation: ''
    })
    
    const errorMessage = ref('')
    const successMessage = ref('')
    const loading = ref(false)

    const handleSignup = async () => {
      errorMessage.value = ''
      successMessage.value = ''

      if (signupForm.value.password !== signupForm.value.password_confirmation) {
        errorMessage.value = '비밀번호가 일치하지 않습니다.'
        return
      }

      if (signupForm.value.password.length < 8) {
        errorMessage.value = '비밀번호는 최소 8자 이상이어야 합니다.'
        return
      }

      loading.value = true

      try {
        await authStore.signup(signupForm.value)
        successMessage.value = '회원가입이 완료되었습니다! 로그인 중...'
      } catch (error) {
        if (error.response?.data) {
          const errors = error.response.data
          if (errors.username) {
            errorMessage.value = '이미 사용 중인 사용자 이름입니다.'
          } else if (errors.email) {
            errorMessage.value = '유효한 이메일 주소를 입력해주세요.'
          } else if (errors.nickname) {
            errorMessage.value = '이미 사용 중인 닉네임입니다.'
          } else if (errors.password) {
            errorMessage.value = errors.password[0] || '비밀번호가 유효하지 않습니다.'
          } else {
            errorMessage.value = '회원가입에 실패했습니다. 다시 시도해주세요.'
          }
        } else {
          errorMessage.value = '회원가입에 실패했습니다. 다시 시도해주세요.'
        }
      } finally {
        loading.value = false
      }
    }

    return {
      signupForm,
      errorMessage,
      successMessage,
      loading,
      handleSignup
    }
  }
}
</script>

<style scoped>
/* HomePage.vue와 같은 스타일 사용 */
.signup-page {
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

.logo-section a {
  text-decoration: none;
}

.logo {
  font-size: 42px;
  font-weight: 900;
  color: #e50914;
  letter-spacing: 3px;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  cursor: pointer;
}

.signup-container {
  position: relative;
  z-index: 10;
  background: rgba(0, 0, 0, 0.75);
  padding: 60px 68px 40px;
  border-radius: 4px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.signup-title {
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

.success-message {
  background: #46d369;
  color: #ffffff;
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 16px;
  font-size: 14px;
}

.signup-form {
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

.signup-button {
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

.signup-button:hover:not(:disabled) {
  background: #f40612;
}

.signup-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.divider {
  text-align: center;
  color: #8c8c8c;
  margin: 20px 0;
  font-size: 14px;
}

.login-link {
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

.login-link:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #ffffff;
}

@media (max-width: 768px) {
  .signup-container {
    padding: 40px 30px;
    margin: 0 20px;
  }
  
  .logo {
    font-size: 32px;
    left: 20px;
  }
}
</style>