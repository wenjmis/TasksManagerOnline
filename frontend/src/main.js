import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

// 設定 API 基礎 URL
axios.defaults.baseURL = 'http://localhost:5000'

const app = createApp(App)
app.config.globalProperties.$http = axios
app.mount('#app')