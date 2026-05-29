import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useTicketEventsStore = defineStore('ticketEvents', () => {
  const refreshCounter = ref(0)

  function triggerRefresh() {
    refreshCounter.value++
  }

  return {
    refreshCounter,
    triggerRefresh,
  }
})
