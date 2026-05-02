<template>
  <form @submit.prevent="register" class="bg-green-100 max-w-min p-2">
    <div class="flex flex-col">
      <label for="username">Username</label>
      <input
        id="username"
        class="border border-green-800 rounded"
        v-model="formData.username"
        type="text"
      />
    </div>
    <div class="flex flex-col">
      <label for="email">Email</label>
      <input
        id="email"
        class="border border-green-800 rounded"
        v-model="formData.email"
        type="email"
      />
    </div>
    <div class="flex flex-col">
      <label for="password">Password</label>
      <input
        id="password"
        class="border border-green-800 rounded"
        v-model="formData.password"
        type="password"
      />
    </div>
    <button :disabled="loading" class="bg-green-800 text-white rounded w-full mt-2 font-bold">
      Register
    </button>
    <RouterLink to="/login">Login</RouterLink>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = reactive({ username: '', email: '', password: '' })
const loading = ref(false)
const errorMessage = ref('')

async function register() {
  errorMessage.value = ''
  loading.value = true
  try {
    await authStore.register(formData.username, formData.email, formData.password)
    router.push('/login?registered=true') // TODO: Show success message on login page
  } catch (error) {
    errorMessage.value = error.message || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
