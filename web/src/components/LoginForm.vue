<template>
  <form @submit.prevent="login" class="bg-indigo-100 max-w-min p-2">
    <BaseInput id="username" label="Username" required v-model="formData.username" />
    <BaseInput
      id="password"
      label="Password"
      type="password"
      required
      v-model="formData.password"
    />
    <button :disabled="loading" class="bg-indigo-800 text-white rounded w-full mt-2 font-bold">
      Login
    </button>
    <RouterLink to="/register">Register</RouterLink>
  </form>
</template>

<script setup>
import BaseInput from '@/components/ui/inputs/BaseInput.vue'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const formData = reactive({ username: '', password: '' })
const loading = ref(false)

async function login() {
  loading.value = true
  try {
    await authStore.login(formData.username, formData.password)
    router.push('/boards')
  } catch (error) {
    notificationStore.error(error.message || 'Login failed. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>
