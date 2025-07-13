import axios from 'axios'

// API 基礎配置
const API_BASE_URL = process.env.NODE_ENV === 'production' 
    ? '/api' // 生產環境使用相對路徑
    : 'http://localhost:5000/api' // 開發環境使用完整 URL

// 創建 axios 實例
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
})

// 請求攔截器
apiClient.interceptors.request.use(
    (config) => {
        // 可以在這裡添加認證 token 等
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// 響應攔截器
apiClient.interceptors.response.use(
    (response) => {
        return response
    },
    (error) => {
        // 統一錯誤處理
        console.error('API Error:', error)
        return Promise.reject(error)
    }
)

export default apiClient