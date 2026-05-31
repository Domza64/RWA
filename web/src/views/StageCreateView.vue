<template>
  <BaseModal title="Create stage" @close="handleClose">
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-4">
      <BaseInput id="name" label="Stage Name" required v-model="formData.name" />

      <div class="flex justify-end mt-4">
        <button
          type="button"
          class="mr-2 px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
          @click="handleClose"
        >
          Cancel
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:opacity-50"
          :disabled="submitting"
        >
          {{ submitting ? 'Creating...' : 'Create Stage' }}
        </button>
      </div>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseInput from '@/components/ui/inputs/BaseInput.vue'
import { createWorkflowStage } from '@/services/boards'
import { useNotificationStore } from '@/stores/notification'
import { useTicketEventsStore } from '@/stores/ticketEvents'

const router = useRouter()
const route = useRoute()
const notificationStore = useNotificationStore()

const boardId = parseInt(route.params.board_id as string)

const submitting = ref(false)

const formData = reactive({
  name: '',
})

function handleClose(): void {
  router.back()
}

async function handleSubmit(): Promise<void> {
  if (!formData.name) {
    notificationStore.error('Please enter a stage name')
    return
  }

  submitting.value = true
  try {
    await createWorkflowStage(boardId, formData.name)
    notificationStore.success('Stage created successfully')

    const ticketEventsStore = useTicketEventsStore()
    ticketEventsStore.triggerRefresh()

    router.back()
  } catch (error) {
    notificationStore.error(error instanceof Error ? error.message : 'Failed to create stage')
  } finally {
    submitting.value = false
  }
}
</script>
