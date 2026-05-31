<script setup lang="ts">
import type { Ticket, WorkflowStage } from '@/types/ticket'

const props = defineProps<{ ticket: Ticket }>()
const emit = defineEmits<{
  (e: 'changeStage', stage: WorkflowStage): void
  (e: 'changeAssignee'): void
  (e: 'changeDueDate'): void
}>()

const URGENCY_LABELS: Record<number, string> = {
  1: 'Very Low',
  2: 'Low',
  3: 'Medium',
  4: 'High',
  5: 'Critical',
}

const URGENCY_CLASSES: Record<number, string> = {
  1: 'bg-gray-200 text-gray-700',
  2: 'bg-indigo-400 text-white',
  3: 'bg-yellow-400 text-black',
  4: 'bg-orange-400 text-black',
  5: 'bg-red-500 text-white',
}

function urgencyLabel(u: number) {
  return URGENCY_LABELS[u] ?? 'Unknown'
}
function urgencyClass(u: number) {
  return URGENCY_CLASSES[u] ?? URGENCY_CLASSES[1]
}

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString()
}
</script>

<template>
  <aside class="flex flex-col gap-6">
    <!-- Stage -->
    <div class="border-4 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div class="bg-black text-white font-black uppercase tracking-wider text-xs px-3 py-2">
        Stage
      </div>
      <div class="p-3 flex flex-col gap-2">
        <div class="font-black uppercase text-sm">
          {{ ticket.current_stage?.name ?? 'No stage' }}
        </div>
        <div class="flex flex-col gap-1 mt-1">
          <button
            v-for="stage in ticket.possible_stages"
            :key="stage.stage_id"
            :class="
              stage.stage_id === ticket.current_stage?.stage_id
                ? 'bg-black text-white cursor-default'
                : 'bg-white hover:bg-yellow-400 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-none hover:translate-x-0.5 hover:translate-y-0.5'
            "
            class="border-2 border-black font-black uppercase text-xs px-3 py-1.5 text-left transition-all"
            :disabled="stage.stage_id === ticket.current_stage?.stage_id"
            @click="emit('changeStage', stage)"
          >
            {{ stage.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- Assignee -->
    <div class="border-4 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div class="bg-black text-white font-black uppercase tracking-wider text-xs px-3 py-2">
        Assignee
      </div>
      <div class="p-3">
        <div class="font-black uppercase text-sm mb-2">
          {{ ticket.assignee?.username ?? 'Unassigned' }}
        </div>
        <button
          class="border-2 border-black font-black uppercase text-xs px-3 py-1.5 bg-white hover:bg-yellow-400 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-none transition-all"
          @click="emit('changeAssignee')"
        >
          {{ ticket.assignee ? 'Change' : 'Assign' }}
        </button>
      </div>
    </div>

    <!-- Reporter -->
    <div class="border-4 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div class="bg-black text-white font-black uppercase tracking-wider text-xs px-3 py-2">
        Reporter
      </div>
      <div class="p-3 font-black uppercase text-sm">
        {{ ticket.reporter?.username ?? '—' }}
      </div>
    </div>

    <!-- Due Date -->
    <div class="border-4 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div class="bg-black text-white font-black uppercase tracking-wider text-xs px-3 py-2">
        Due Date
      </div>
      <div class="p-3">
        <div class="font-black uppercase text-sm mb-2">{{ formatDate(ticket.due_date) }}</div>
        <button
          class="border-2 border-black font-black uppercase text-xs px-3 py-1.5 bg-white hover:bg-yellow-400 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-none transition-all"
          @click="emit('changeDueDate')"
        >
          Edit
        </button>
      </div>
    </div>

    <!-- Urgency -->
    <div class="border-4 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]">
      <div class="bg-black text-white font-black uppercase tracking-wider text-xs px-3 py-2">
        Urgency
      </div>
      <div class="p-3">
        <span
          class="border-2 border-black font-black uppercase text-xs px-3 py-1.5 inline-block"
          :class="urgencyClass(ticket.urgency)"
        >
          {{ urgencyLabel(ticket.urgency) }}
        </span>
      </div>
    </div>
  </aside>
</template>
