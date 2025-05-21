import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/global.css'; // 引入全局 CSS 文件
import Vue3Lottie from 'vue3-lottie'
const app = createApp(App)
app.use(Vue3Lottie)
app.mount('#app')
