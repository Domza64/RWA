<template>
  <BaseModal title="Create ticket" @close="handleClose">
    <form @submit.prevent="handleSubmit" class="flex flex-col gap-4">
        <BaseInput id="title" label="Title" required v-model="formData.title" />
        <BaseInput id="description" label="Description" required v-model="formData.description" />

        <BaseInput id="due_date" type="date" label="Due Date" v-model="formData.due_date" />

        <BaseSelect
          id="urgency"
          label="Urgency"
          required
          :options="urgencyOptions"
          v-model="formData.urgency"
        />

        <BaseSelect
          id="asignee_id"
          label="Assignee"
          :options="assigneeOptions"
          v-model="formData.asignee_id"
          placeholder="Select assignee"
        />

        <BaseSelect
          id="current_stage"
          label="Current Stage"
          :options="stageOptions"
          v-model="formData.current_stage"
          placeholder="Select stage"
        />

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
            {{ submitting ? 'Creating...' : 'Create Ticket' }}
          </button>
        </div>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseModal from '@/components/ui/BaseModal.vue'
import BaseInput from '@/components/ui/inputs/BaseInput.vue'
import BaseSelect from '@/components/ui/inputs/BaseSelect.vue'
import type { SelectOption } from '@/components/ui/inputs/BaseSelect.vue'
import { getMembers, getWorkflowStages } from '@/services/boards'
import { createTicket } from '@/services/tickets'
import type { Member } from '@/types/board'
import type { WorkflowStage } from '@/types/ticket'
import { useNotificationStore } from '@/stores/notification'
import { useTicketEventsStore } from '@/stores/ticketEvents'

const router = useRouter()
const route = useRoute()
const notificationStore = useNotificationStore()

const boardId = parseInt(route.params.board_id as string)

const submitting = ref(false)
const members = ref<Member[]>([])
const stages = ref<WorkflowStage[]>([])

const formData = reactive({
  title: '',
  description: '',
  due_date: '',
  urgency: 1,
  asignee_id: '' as string | number,
  current_stage: '' as string | number,
})

const urgencyOptions: SelectOption[] = [
  { value: 1, label: '1 - Very Low' },
  { value: 2, label: '2 - Low' },
  { value: 3, label: '3 - Medium' },
  { value: 4, label: '4 - High' },
  { value: 5, label: '5 - Critical' },
]

const assigneeOptions = computed<SelectOption[]>(() =>
  members.value.map((m) => ({
    value: m.user.user_id,
    label: m.user.username,
  })),
)

const stageOptions = computed<SelectOption[]>(() =>
  stages.value.map((s) => ({
    value: s.stage_id,
    label: s.name,
  })),
)

async function loadData() {
  try {
    const [m, s] = await Promise.all([getMembers(boardId), getWorkflowStages(boardId)])
    members.value = m
    stages.value = s
  } catch (error) {
    notificationStore.error('Failed to load board details')
  }
}

onMounted(() => {
  loadData()
})

function handleClose(): void {
  router.back()
}

async function handleSubmit(): Promise<void> {
  if (!formData.title || !formData.description) {
    notificationStore.error('Please fill out all required fields')
    return
  }

  submitting.value = true
  try {
    await createTicket(
      boardId,
      formData.title,
      formData.description,
      Number(formData.urgency),
      formData.due_date || null,
      formData.asignee_id ? Number(formData.asignee_id) : null,
      formData.current_stage ? Number(formData.current_stage) : null,
    )
    notificationStore.success('Ticket created successfully')

    const ticketEventsStore = useTicketEventsStore()
    ticketEventsStore.triggerRefresh()

    router.back()
  } catch (error) {
    notificationStore.error(error instanceof Error ? error.message : 'Failed to create ticket')
  } finally {
    submitting.value = false
  }
}
</script>
