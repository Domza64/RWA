<template>
  <form @submit.prevent="login" class="flex flex-col gap-5 text-left">
    <BaseInput id="username" label="Username" required v-model="formData.username" />
    <BaseInput
      id="password"
      label="Password"
      type="password"
      required
      v-model="formData.password"
    />
    <button
      :disabled="loading"
      class="mt-2 border-4 border-black bg-indigo-600 hover:bg-indigo-700 text-white font-black uppercase tracking-wider py-3 px-4 transition-transform active:translate-y-1 disabled:opacity-70 disabled:active:translate-y-0"
    >
      {{ loading ? 'Authenticating...' : 'Login' }}
    </button>
    
    <div class="text-center mt-2 border-t-4 border-black pt-4 font-bold">
      <RouterLink to="/register" class="hover:underline hover:text-indigo-600 uppercase">
        Create an account
      </RouterLink>
    </div>
  </form>
</template>

<script setup lang="ts">
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
    notificationStore.error(
      error instanceof Error ? error.message : 'Login failed. Please try again.',
    )
  } finally {
    loading.value = false
  }
}
</script>
