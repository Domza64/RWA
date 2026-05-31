<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  getTicket,
  updateTicketStage,
  updateTicketDescription,
  updateTicketDueDate,
} from '@/services/tickets'
import { useNotificationStore } from '@/stores/notification'
import type { Ticket, WorkflowStage } from '@/types/ticket'
import TicketMeta from '@/components/ticket/TicketMeta.vue'
import TicketDescription from '@/components/ticket/TicketDescription.vue'

const route = useRoute()
const router = useRouter()
const notificationStore = useNotificationStore()

const boardId = route.params.board_id as string
const ticketId = parseInt(route.params.ticket_id as string)

const ticket = ref<Ticket | null>(null)
const loading = ref(true)

async function load() {
  loading.value = true
  try {
    ticket.value = await getTicket(ticketId)
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Failed to load ticket.')
  } finally {
    loading.value = false
  }
}

async function onChangeStage(stage: WorkflowStage) {
  if (!ticket.value) return
  try {
    await updateTicketStage(ticketId, stage.stage_id)
    ticket.value.current_stage = stage
    notificationStore.success?.('Stage updated.')
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Failed to update stage.')
  }
}

async function onSaveDescription(value: string) {
  try {
    await updateTicketDescription(ticketId, value)
    if (ticket.value) ticket.value.description = value
    notificationStore.success?.('Description updated.')
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Failed to update description.')
  }
}

async function onSaveDueDate(date: string) {
  try {
    await updateTicketDueDate(ticketId, date || null)
    if (ticket.value) ticket.value.due_date = date
    notificationStore.success?.('Due date updated.')
  } catch (e) {
    notificationStore.error(e instanceof Error ? e.message : 'Failed to update due date.')
  }
}

// Placeholder: opens assignee picker (no backend yet)
function onChangeAssignee() {
  notificationStore.error('Assignee editing not yet implemented.')
}

// Placeholder: opens date picker inline via TicketMeta
const editingDueDate = ref(false)
const dueDateDraft = ref('')

function onChangeDueDate() {
  dueDateDraft.value = ticket.value?.due_date ?? ''
  editingDueDate.value = true
}

function saveDueDate() {
  onSaveDueDate(dueDateDraft.value)
  editingDueDate.value = false
}

onMounted(load)
</script>

<template>
  <div class="min-h-[calc(100vh-3.5rem)] p-6">
    <!-- Loading -->
    <div
      v-if="loading"
      class="font-black uppercase text-xl tracking-widest animate-pulse p-6 bg-yellow-400 border-4 border-black inline-block shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
    >
      Loading...
    </div>

    <!-- Not found -->
    <div
      v-else-if="!ticket"
      class="font-black uppercase border-4 border-black p-6 bg-yellow-400 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
    >
      Ticket not found.
    </div>

    <template v-else>
      <!-- Back link -->
      <RouterLink
        :to="`/boards/${boardId}`"
        class="inline-block mb-6 font-black uppercase text-sm border-2 border-black px-3 py-1.5 bg-white hover:bg-yellow-400 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-none transition-all"
      >
        ← Back to Board
      </RouterLink>

      <div class="grid grid-cols-1 lg:grid-cols-[1fr_280px] gap-8">
        <!-- Left: main content -->
        <div class="flex flex-col gap-8">
          <!-- Title -->
          <div class="border-b-4 border-black pb-6">
            <div class="text-xs font-black uppercase text-gray-500 mb-1">
              #{{ ticket.ticket_id }}
            </div>
            <h1 class="text-4xl font-black uppercase tracking-tight leading-tight">
              {{ ticket.title }}
            </h1>
          </div>

          <!-- Description -->
          <section
            class="border-4 border-black bg-white shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] p-6"
          >
            <h2
              class="font-black uppercase tracking-wider text-sm border-b-4 border-black pb-2 mb-4"
            >
              Description
            </h2>
            <TicketDescription
              :model-value="ticket.description"
              @update:model-value="(v) => (ticket!.description = v)"
              @save="onSaveDescription(ticket!.description)"
              @cancel="() => {}"
            />
          </section>
        </div>

        <!-- Right: meta sidebar -->
        <div class="flex flex-col gap-4">
          <TicketMeta
            :ticket="ticket"
            @change-stage="onChangeStage"
            @change-assignee="onChangeAssignee"
            @change-due-date="onChangeDueDate"
          />

          <!-- Due date edit (inline, shown when editing) -->
          <div
            v-if="editingDueDate"
            class="border-4 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] p-4 flex flex-col gap-3"
          >
            <label class="font-black uppercase text-xs">New Due Date</label>
            <input
              v-model="dueDateDraft"
              type="date"
              class="border-4 border-black p-2 font-medium focus:outline-none focus:bg-indigo-50"
            />
            <div class="flex gap-2">
              <button
                class="border-4 border-black bg-indigo-600 text-white font-black uppercase text-xs px-3 py-1.5 hover:bg-black transition-all shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] active:shadow-none"
                @click="saveDueDate"
              >
                Save
              </button>
              <button
                class="border-4 border-black bg-white font-black uppercase text-xs px-3 py-1.5 hover:bg-yellow-400 transition-all shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] active:shadow-none"
                @click="editingDueDate = false"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
