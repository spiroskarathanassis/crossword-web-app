import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

// config global variables
app.config.globalProperties = {
  'is_testing' : 0, // IS_TESTING_DATA
  'is_admin': 0, // IS_SHOWING_ANSWERS
  'pdf_title': 'driver'
}

app.mount('#app')
