<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { createBoard } from '@/services/boards'
import BaseInput from '@/components/ui/inputs/BaseInput.vue'

const router = useRouter()

const formData = reactive({ name: '', description: '' })
const loading = ref(false)
const errorMessage = ref('')

async function submit() {
  loading.value = true
  errorMessage.value = ''
  try {
    const boardId = await createBoard(formData.name, formData.description)
    router.push(`/boards/${boardId}`)
  } catch (error: any) {
    errorMessage.value = error.message || 'Failed to create board.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="text-center my-24 flex flex-col items-center">
    <h1 class="text-4xl font-bold mb-4">Create board</h1>

    <form @submit.prevent="submit" class="bg-indigo-100 p-4 rounded text-left min-w-75">
      <BaseInput id="name" label="Board Name" required v-model="formData.name" />
      <BaseInput id="description" label="Description" required v-model="formData.description" />

      <p v-if="errorMessage" class="text-red-600 mt-2">{{ errorMessage }}</p>

      <button :disabled="loading" class="bg-indigo-800 text-white rounded w-full mt-4 p-2 font-bold">
        {{ loading ? 'Creating...' : 'Create Board' }}
      </button>
    </form>
  </section>
</template>
