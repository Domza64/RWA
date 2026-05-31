<template>
  <div class="border-4 border-black bg-white p-3 hover:bg-yellow-400 hover:-translate-y-0.5 hover:-translate-x-0.5 transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] cursor-pointer">
    <!-- Title -->
    <div class="text-sm font-black uppercase leading-snug mb-2">
      {{ data.title }}
    </div>

    <!-- Meta row -->
    <div class="flex items-center justify-between text-xs font-bold">
      <!-- Due date -->
      <span class="text-gray-700">{{ formatDate(data.due_date) }}</span>

      <!-- Urgency -->
      <span class="px-2 py-0.5 border-2 border-black text-xs font-black uppercase" :class="urgencyClass">
        {{ urgencyLabel }}
      </span>
    </div>

    <!-- Assignee -->
    <div class="mt-2 flex items-center justify-between border-t-2 border-black pt-2">
      <div class="text-xs font-black text-gray-500">#{{ data.ticket_id }}</div>

      <div
        v-if="data.assignee"
        class="text-xs font-black uppercase truncate max-w-[120px]"
        :title="data.assignee.username"
      >
        {{ data.assignee.username }}
      </div>

      <div v-else class="text-xs font-black uppercase text-gray-400">Unassigned</div>
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

  if (u >= 5) return 'bg-red-500 text-white'
  if (u === 4) return 'bg-orange-400 text-black'
  if (u === 3) return 'bg-yellow-400 text-black'
  if (u === 2) return 'bg-indigo-400 text-white'
  return 'bg-gray-200 text-gray-700'
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
