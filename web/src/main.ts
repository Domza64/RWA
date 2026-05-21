import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useNotificationStore } from './stores/notification'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.config.errorHandler = (err) => {
  const message = err instanceof Error ? err.message : 'Unexpected error.'
  useNotificationStore(pinia).error(message)
}

app.mount('#app')
