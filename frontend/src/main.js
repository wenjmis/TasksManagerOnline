import { createApp } from 'vue'
import App from './App.vue'
import apiClient from './api/config'

const app = createApp(App)
app.config.globalProperties.$http = apiClient
app.mount('#app')