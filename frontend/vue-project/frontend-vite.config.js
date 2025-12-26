import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  // Vue 플러그인 사용
  plugins: [vue()],
  
  // 경로 별칭 설정 (@를 src 디렉토리로 매핑)
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  
  // 개발 서버 설정
  server: {
    port: 5173,  // 개발 서버 포트
    host: true,  // 모든 네트워크 인터페이스에서 접근 가능
    proxy: {
      // API 요청을 백엔드로 프록시 (개발 환경)
      '/api': {
        target: process.env.VITE_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  
  // 프로덕션 빌드 설정
  build: {
    outDir: 'dist',  // 빌드 출력 디렉토리
    assetsDir: 'assets',  // 정적 파일 디렉토리
    sourcemap: false,  // 소스맵 비활성화 (번들 크기 최소화)
    minify: 'terser',  // 코드 압축
    chunkSizeWarningLimit: 1000,  // 청크 크기 경고 임계값
    rollupOptions: {
      output: {
        // 청크 파일 이름 패턴
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
      }
    }
  },
  
  // 프리뷰 서버 설정 (빌드 후 미리보기)
  preview: {
    port: 4173,  // 프리뷰 서버 포트
    host: true,  // 모든 네트워크 인터페이스에서 접근 가능
  }
})
