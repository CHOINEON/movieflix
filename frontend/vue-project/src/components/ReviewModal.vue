<!-- frontend/src/components/ReviewModal.vue -->

<template>
  <Transition name="modal">
    <div v-if="show" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <!-- 닫기 버튼 -->
        <button class="close-btn" @click="closeModal">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>

        <!-- 제목 -->
        <h2 class="modal-title">{{ movieTitle }}</h2>

        <!-- 별점 선택 -->
        <div class="rating-section">
          <div class="rating-label">{{ ratingText }}</div>
          <div class="stars">
            <button
              v-for="star in 5"
              :key="star"
              class="star-btn"
              :class="{ 'active': star <= rating }"
              @click="setRating(star)"
            >
              ⭐
            </button>
          </div>
        </div>

        <!-- 리뷰 입력 -->
        <div class="review-section">
          <textarea
            v-model="content"
            class="review-textarea"
            placeholder="이 콘텐츠의 어떤 점이 좋거나 싫었는지 다른 사용자들에게 알려주세요. 고객님의 리뷰는 다른 사용자들에게 큰 도움이 됩니다."
            maxlength="2000"
          ></textarea>
          <div class="char-count">{{ content.length }} / 2000</div>
        </div>

        <!-- 에러 메시지 -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- 등록/수정 버튼 -->
        <button 
          class="submit-btn"
          :disabled="!canSubmit || loading"
          @click="submitReview"
        >
          {{ loading ? (isEditMode ? '수정 중...' : '등록 중...') : (isEditMode ? '수정하기' : '등록하기') }}
        </button>
      </div>
    </div>
  </Transition>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { movieAPI } from '@/api/movies'

export default {
  name: 'ReviewModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    movieId: {
      type: Number,
      required: true
    },
    movieTitle: {
      type: String,
      required: true
    },
    editReview: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'review-created', 'review-updated'],
  setup(props, { emit }) {
    const rating = ref(5)
    const content = ref('')
    const isSpoiler = ref(false)
    const loading = ref(false)
    const error = ref(null)

    const isEditMode = computed(() => {
      return props.editReview !== null
    })

    const ratingText = computed(() => {
      return `${rating.value}.0 최고`
    })

    const canSubmit = computed(() => {
      return rating.value > 0 && content.value.trim().length >= 10
    })

    const setRating = (star) => {
      rating.value = star
    }

    const resetForm = () => {
      rating.value = 5
      content.value = ''
      isSpoiler.value = false
      error.value = null
    }

    const loadReviewData = () => {
      if (props.editReview) {
        rating.value = props.editReview.rating
        content.value = props.editReview.content
        isSpoiler.value = props.editReview.is_spoiler
        console.log('✏️ 수정할 리뷰 데이터 로드:', props.editReview)
      } else {
        resetForm()
      }
    }

    const submitReview = async () => {
      if (!canSubmit.value) return

      const reviewData = {
        rating: rating.value,
        content: content.value.trim(),
        is_spoiler: isSpoiler.value
      }

      loading.value = true
      error.value = null

      try {
        if (isEditMode.value) {
          // 수정 모드
          console.log('✏️ 리뷰 수정:', reviewData)
          const response = await movieAPI.updateReview(props.editReview.id, reviewData)
          console.log('✅ 리뷰 수정 성공:', response.data)
          emit('review-updated', response.data)
        } else {
          // 작성 모드
          console.log('📝 리뷰 작성:', reviewData)
          const response = await movieAPI.createReview(props.movieId, reviewData)
          console.log('✅ 리뷰 작성 성공:', response.data)
          emit('review-created', response.data)
        }
        
        resetForm()
      } catch (err) {
        console.error('❌ 리뷰 작성/수정 실패:', err)
        error.value = err.response?.data?.error || '리뷰 작성/수정에 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    const closeModal = () => {
      resetForm()
      emit('close')
    }

    // editReview가 변경될 때마다 폼 데이터 로드
    watch(() => props.editReview, () => {
      if (props.show) {
        loadReviewData()
      }
    }, { immediate: true })

    // 모달이 열릴 때마다 폼 데이터 로드
    watch(() => props.show, (newVal) => {
      if (newVal) {
        loadReviewData()
      }
    })

    return {
      rating,
      content,
      isSpoiler,
      loading,
      error,
      isEditMode,
      ratingText,
      canSubmit,
      setRating,
      submitReview,
      closeModal
    }
  }
}
</script>

<style scoped>
/* 모달 트랜지션 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}

/* 오버레이 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

/* 모달 컨테이너 */
.modal-container {
  background: #181818;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  padding: 40px;
  position: relative;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.7);
}

/* 닫기 버튼 */
.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* 제목 */
.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: white;
  margin: 0 0 32px 0;
}

/* 별점 섹션 */
.rating-section {
  margin-bottom: 32px;
}

.rating-label {
  font-size: 20px;
  font-weight: 600;
  color: white;
  margin-bottom: 16px;
}

.stars {
  display: flex;
  gap: 8px;
}

.star-btn {
  background: none;
  border: none;
  font-size: 32px;
  cursor: pointer;
  opacity: 0.3;
  transition: all 0.2s;
  padding: 0;
}

.star-btn.active {
  opacity: 1;
  transform: scale(1.1);
}

.star-btn:hover {
  transform: scale(1.2);
}

/* 리뷰 섹션 */
.review-section {
  margin-bottom: 24px;
}

.review-textarea {
  width: 100%;
  min-height: 200px;
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
  border-radius: 8px;
  padding: 16px;
  color: white;
  font-size: 14px;
  font-family: inherit;
  line-height: 1.6;
  resize: vertical;
  transition: border-color 0.2s;
}

.review-textarea:focus {
  outline: none;
  border-color: #e50914;
}

.review-textarea::placeholder {
  color: #666;
}

.char-count {
  text-align: right;
  color: #888;
  font-size: 12px;
  margin-top: 8px;
}

/* 스포일러 섹션 */
.spoiler-section {
  margin-bottom: 24px;
}

.spoiler-checkbox {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  color: #e5e5e5;
  font-size: 14px;
}

.spoiler-checkbox input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #e50914;
}

/* 에러 메시지 */
.error-message {
  background: rgba(229, 9, 20, 0.1);
  border: 1px solid #e50914;
  border-radius: 6px;
  padding: 12px 16px;
  color: #ff4d4d;
  font-size: 14px;
  margin-bottom: 24px;
}

/* 등록 버튼 */
.submit-btn {
  width: 100%;
  padding: 16px;
  background: #00a8e1;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #0099cc;
}

.submit-btn:disabled {
  background: #333;
  color: #666;
  cursor: not-allowed;
}

/* 반응형 */
@media (max-width: 768px) {
  .modal-container {
    padding: 32px 24px;
    max-height: 90vh;
    overflow-y: auto;
  }

  .modal-title {
    font-size: 20px;
    margin-bottom: 24px;
  }

  .rating-label {
    font-size: 18px;
  }

  .star-btn {
    font-size: 28px;
  }

  .review-textarea {
    min-height: 150px;
  }
}
</style>