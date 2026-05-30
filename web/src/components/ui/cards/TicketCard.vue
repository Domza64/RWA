<template>
  <div
    class="rounded-md border border-gray-200 bg-gray-50 shadow p-3 hover:border-gray-300 transition"
  >
    <!-- Title -->
    <div class="text-sm font-semibold text-gray-800 leading-snug">
      {{ data.title }}
    </div>

    <!-- Meta row -->
    <div class="mt-2 flex items-center justify-between text-xs text-gray-500">
      <!-- Due date -->
      <span> Due: {{ formatDate(data.due_date) }} </span>

      <!-- Urgency -->
      <span class="px-2 py-0.5 rounded-full text-xs font-medium" :class="urgencyClass">
        {{ urgencyLabel }}
      </span>
    </div>

    <!-- Assignee -->
    <div class="mt-3 flex items-center justify-between">
      <div class="text-xs text-gray-400">#{{ data.ticket_id }}</div>

      <div
        v-if="data.assignee"
        class="text-xs text-gray-600 font-medium truncate max-w-[120px]"
        :title="data.assignee.username"
      >
        {{ data.assignee.username }}
      </div>

      <div v-else class="text-xs text-gray-300">Unassigned</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SimpleTicket } from '@/types/ticket'
import { computed } from 'vue'

interface Props {
  data: SimpleTicket
}

const props = defineProps<Props>()

function formatDate(date: string) {
  if (!date) return '—'
  return new Date(date).toLocaleDateString()
}

const urgencyClass = computed(() => {
  const u = props.data.urgency

  if (u >= 5) return 'bg-red-100 text-red-700'
  if (u === 4) return 'bg-orange-100 text-orange-600'
  if (u === 3) return 'bg-yellow-100 text-yellow-700'
  if (u === 2) return 'bg-indigo-100 text-indigo-600'
  return 'bg-indigo-50 text-indigo-400'
})

const urgencyLabel = computed(() => {
  const u = props.data.urgency
  if (u >= 5) return 'Critical'
  if (u === 4) return 'High'
  if (u === 3) return 'Medium'
  if (u === 2) return 'Low'
  return 'Very Low'
})
</script>
