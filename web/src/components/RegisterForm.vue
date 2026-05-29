<template>
  <form @submit.prevent="register" class="bg-green-100 max-w-min p-2">
    <BaseInput id="username" label="Username" v-model="formData.username" />
    <BaseInput id="email" label="Email" type="email" v-model="formData.email" />
    <BaseInput id="password" label="Password" type="password" v-model="formData.password" />
    <button :disabled="loading" class="bg-green-800 text-white rounded w-full mt-2 font-bold">
      Register
    </button>
    <RouterLink to="/login">Login</RouterLink>
  </form>
</template>

<script setup>
import BaseInput from '@/components/ui/BaseInput.vue'
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
