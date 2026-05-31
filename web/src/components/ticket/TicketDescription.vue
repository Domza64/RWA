<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'save'): void
  (e: 'cancel'): void
}>()

const editing = ref(false)
const draft = ref(props.modelValue)

watch(() => props.modelValue, (v) => { draft.value = v })

function startEdit() {
  draft.value = props.modelValue
  editing.value = true
}

function save() {
  emit('update:modelValue', draft.value)
  emit('save')
  editing.value = false
}

function cancel() {
  emit('cancel')
  editing.value = false
}
</script>

<template>
  <div>
    <div v-if="!editing">
      <p class="font-bold text-gray-800 whitespace-pre-wrap leading-relaxed min-h-[3rem]">
        {{ modelValue || 'No description provided.' }}
      </p>
      <button
        class="mt-3 border-2 border-black font-black uppercase text-xs px-3 py-1.5 bg-white hover:bg-yellow-400 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-none transition-all"
        @click="startEdit"
      >
        Edit
      </button>
    </div>

    <div v-else class="flex flex-col gap-3">
      <textarea
        v-model="draft"
        rows="6"
        class="border-4 border-black p-3 font-medium focus:outline-none focus:bg-indigo-50 resize-none w-full"
      />
      <div class="flex gap-3">
        <button
          class="border-4 border-black bg-indigo-600 text-white font-black uppercase tracking-wider px-4 py-2 hover:bg-black transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 text-sm"
          @click="save"
        >
          Save
        </button>
        <button
          class="border-4 border-black bg-white text-black font-black uppercase tracking-wider px-4 py-2 hover:bg-yellow-400 transition-all shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] active:shadow-none active:translate-x-1 active:translate-y-1 text-sm"
          @click="cancel"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>
