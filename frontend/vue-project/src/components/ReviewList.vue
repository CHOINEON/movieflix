<!-- frontend/src/components/ReviewList.vue -->

<template>
  <div class="review-list">
    <!-- 헤더 -->
    <div class="review-header">
      <h3 class="section-title">리뷰</h3>
      <button class="write-review-btn" @click="openReviewModal">
        리뷰 작성
      </button>
    </div>

    <!-- 로딩 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>리뷰를 불러오는 중...</p>
    </div>

    <!-- 에러 -->
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <!-- 리뷰 목록 -->
    <div v-else-if="reviews.length > 0" class="reviews-container">
      <div 
        v-for="review in reviews" 
        :key="review.id"
        class="review-card"
      >
        <!-- 별점 -->
        <div class="review-rating">
          <span v-for="star in 5" :key="star" class="star">
            {{ star <= review.rating ? '⭐' : '☆' }}
          </span>
        </div>

        <!-- 작성자 및 날짜 -->
        <div class="review-meta">
          <span class="author">{{ review.nickname || review.username }}</span>
          <span class="separator">•</span>
          <span class="date">{{ formatDate(review.created_at) }}</span>
        </div>

        <!-- 리뷰 내용 -->
        <div class="review-content">
          <p>{{ review.content }}</p>
        </div>

        <!-- 액션 버튼들 -->
        <div class="review-actions">
          <!-- 좋아요 버튼 -->
          <button 
            class="like-btn"
            :class="{ 'liked': review.is_liked }"
            @click="toggleLike(review)"
            :disabled="review.is_mine"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z"/>
            </svg>
            <span>{{ review.likes_count }}</span>
          </button>

          <!-- 본인 리뷰면 수정/삭제 버튼 -->
          <div v-if="review.is_mine" class="my-review-actions">
            <button class="edit-btn" @click="editReview(review)">
              수정
            </button>
            <button class="delete-btn" @click="deleteReview(review)">
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 리뷰 없음 -->
    <div v-else class="no-reviews">
      <p>아직 작성된 리뷰가 없습니다.</p>
      <p>첫 번째 리뷰를 작성해보세요!</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { movieAPI } from '@/api/movies'

export default {
  name: 'ReviewList',
  props: {
    movieId: {
      type: Number,
      required: true
    }
  },
  emits: ['open-review-modal', 'edit-review'],
  setup(props, { emit }) {
    const reviews = ref([])
    const loading = ref(false)
    const error = ref(null)

    const loadReviews = async () => {
      loading.value = true
      error.value = null

      try {
        console.log('📋 리뷰 목록 로딩:', props.movieId)
        const response = await movieAPI.getMovieReviews(props.movieId)
        reviews.value = response.data
        console.log('✅ 리뷰 목록:', reviews.value)
      } catch (err) {
        console.error('❌ 리뷰 목록 로드 실패:', err)
        error.value = '리뷰를 불러오는데 실패했습니다.'
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}년 ${month}월 ${day}일`
    }

    const openReviewModal = () => {
      emit('open-review-modal')
    }

    const toggleLike = async (review) => {
      if (review.is_mine) return

      try {
        console.log('❤️ 리뷰 좋아요 토글:', review.id)
        const response = await movieAPI.toggleReviewLike(review.id)
        
        // 상태 업데이트
        review.is_liked = response.data.is_liked
        review.likes_count = response.data.likes_count
        
        console.log('✅ 좋아요 토글 성공:', response.data)
      } catch (err) {
        console.error('❌ 좋아요 실패:', err)
      }
    }

    const editReview = (review) => {
      console.log('✏️ 리뷰 수정 시작:', review)
      // 부모 컴포넌트(MovieDetailModal)에게 수정할 리뷰 정보 전달
      emit('edit-review', review)
    }

    const deleteReview = async (review) => {
      if (!confirm('정말 이 리뷰를 삭제하시겠습니까?')) return

      try {
        console.log('🗑️ 리뷰 삭제:', review.id)
        await movieAPI.deleteReview(review.id)
        
        // 목록에서 제거
        reviews.value = reviews.value.filter(r => r.id !== review.id)
        
        console.log('✅ 리뷰 삭제 성공')
      } catch (err) {
        console.error('❌ 리뷰 삭제 실패:', err)
        alert('리뷰 삭제에 실패했습니다.')
      }
    }

    const addReview = (newReview) => {
      // 새 리뷰를 목록 맨 앞에 추가
      reviews.value.unshift(newReview)
    }

    const updateReview = (updatedReview) => {
      // 수정된 리뷰를 목록에서 업데이트
      const index = reviews.value.findIndex(r => r.id === updatedReview.id)
      if (index !== -1) {
        reviews.value[index] = updatedReview
      }
    }

    onMounted(() => {
      loadReviews()
    })

    return {
      reviews,
      loading,
      error,
      formatDate,
      openReviewModal,
      toggleLike,
      editReview,
      deleteReview,
      addReview,
      updateReview
    }
  }
}
</script>

<style scoped>
.review-list {
  margin-top: 40px;
}

/* 헤더 */
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin: 0;
}

.write-review-btn {
  padding: 10px 20px;
  background: #e50914;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.write-review-btn:hover {
  background: #f40612;
}

/* 로딩 */
.loading {
  text-align: center;
  padding: 40px;
  color: #e5e5e5;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #333;
  border-top-color: #e50914;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 에러 */
.error {
  text-align: center;
  padding: 40px;
  color: #ff4d4d;
}

/* 리뷰 없음 */
.no-reviews {
  text-align: center;
  padding: 60px 20px;
  color: #888;
}

.no-reviews p:first-child {
  font-size: 16px;
  margin-bottom: 8px;
}

.no-reviews p:last-child {
  font-size: 14px;
  color: #666;
}

/* 리뷰 컨테이너 */
.reviews-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 리뷰 카드 */
.review-card {
  background: #2a2a2a;
  padding: 20px;
  border-radius: 8px;
}

/* 별점 */
.review-rating {
  margin-bottom: 12px;
}

.star {
  font-size: 18px;
  margin-right: 2px;
}

/* 작성자 및 날짜 */
.review-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}

.author {
  color: #e5e5e5;
  font-weight: 600;
}

.separator {
  color: #666;
}

.date {
  color: #888;
}

/* 리뷰 내용 */
.review-content {
  margin-bottom: 16px;
}

.review-content p {
  color: #e5e5e5;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
  white-space: pre-wrap;
}

/* 액션 버튼들 */
.review-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: #e5e5e5;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.like-btn.liked {
  background: rgba(229, 9, 20, 0.2);
  border-color: #e50914;
  color: #e50914;
}

.like-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 본인 리뷰 액션 */
.my-review-actions {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

.edit-btn,
.delete-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #e5e5e5;
}

.edit-btn:hover {
  background: rgba(255, 255, 255, 0.15);
}

.delete-btn {
  background: rgba(229, 9, 20, 0.2);
  color: #ff4d4d;
}

.delete-btn:hover {
  background: rgba(229, 9, 20, 0.3);
}

/* 반응형 */
@media (max-width: 768px) {
  .review-card {
    padding: 16px;
  }

  .review-actions {
    flex-wrap: wrap;
  }

  .my-review-actions {
    margin-left: 0;
    width: 100%;
  }
}
</style>