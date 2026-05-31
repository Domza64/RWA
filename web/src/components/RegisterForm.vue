<template>
  <form @submit.prevent="register" class="flex flex-col gap-5 text-left">
    <BaseInput id="username" label="Username" v-model="formData.username" />
    <BaseInput id="email" label="Email" type="email" v-model="formData.email" />
    <BaseInput id="password" label="Password" type="password" v-model="formData.password" />
    
    <p v-if="errorMessage" class="text-red-600 font-bold bg-red-100 border-4 border-red-600 p-2 uppercase text-sm tracking-wider">{{ errorMessage }}</p>

    <button
      :disabled="loading"
      class="mt-2 border-4 border-black bg-indigo-600 hover:bg-indigo-700 text-white font-black uppercase tracking-wider py-3 px-4 transition-transform active:translate-y-1 disabled:opacity-70 disabled:active:translate-y-0"
    >
      {{ loading ? 'Creating Account...' : 'Register' }}
    </button>
    <div class="text-center mt-2 border-t-4 border-black pt-4 font-bold">
      <RouterLink to="/login" class="hover:underline hover:text-indigo-600 uppercase">
        Already have an account? Login
      </RouterLink>
    </div>
  </form>
</template>

<script setup lang="ts">
import BaseInput from '@/components/ui/inputs/BaseInput.vue'
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
    errorMessage.value =
      error instanceof Error ? error.message : 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
