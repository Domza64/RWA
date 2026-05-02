<template>
  <form @submit.prevent="login" class="bg-green-100 max-w-min p-2">
    <div class="flex flex-col">
      <label for="username">Username</label>
      <input class="border border-green-800 rounded" v-model="formData.username" type="text" />
    </div>
    <div class="flex flex-col">
      <label for="password">Password</label>
      <input class="border border-green-800 rounded" v-model="formData.password" type="password" />
    </div>
    <button :disabled="loading" class="bg-green-800 text-white rounded w-full mt-2 font-bold">
      Login
    </button>
    <RouterLink to="/register">Register</RouterLink>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = reactive({ username: '', password: '' })
const loading = ref(false)
const errorMessage = ref('')

async function login() {
  errorMessage.value = ''
  loading.value = true
  try {
    await authStore.login(formData.username, formData.password)
    router.push('/boards')
  } catch (error) {
    errorMessage.value = error.message || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
