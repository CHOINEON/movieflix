// frontend/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import HomePage from '@/views/HomePage.vue'
import SignupPage from '@/views/SignupPage.vue'
import MovieListView from '@/views/MovieListView.vue'
import FavoritesView from '@/views/FavoritesView.vue'
import ChatbotView from  '@/views/ChatbotView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
    meta: { requiresGuest: true }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/movies',
    name: 'movies',
    component: MovieListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'favorites',
    component: FavoritesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/chatbot',
    name: 'chatbot',
    component: ChatbotView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'home' })
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'movies' })
  } else {
    next()
  }
})

export default router