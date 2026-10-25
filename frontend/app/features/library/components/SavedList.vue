<script setup lang="ts">
import { useAuth } from '~/features/auth/composables/useAuth'
import { useResumeLibrary } from '../composables/useResumeLibrary'

const { t } = useI18n()
const { isAuthenticated } = useAuth()
const { items, pending, open, remove } = useResumeLibrary()

function labelFor(item: { title: string, target_job: string, id: number }): string {
  return item.title || item.target_job || `#${item.id}`
}
</script>

<template>
  <div
    id="saved"
    class="mt-7"
  >
    <h2 class="mb-3 text-xs font-semibold tracking-wide text-slate-500 uppercase">
      {{ t('saved_title') }}
    </h2>

    <div
      v-if="pending"
      class="text-xs text-slate-500"
    >
      {{ t('saved_loading') }}
    </div>

    <ul
      v-else
      class="flex list-none flex-col gap-1.5"
    >
      <li
        v-if="!isAuthenticated"
        class="text-xs leading-snug text-slate-500"
      >
        {{ t('saved_empty') }}
      </li>
      <li
        v-else-if="!items?.length"
        class="text-xs leading-snug text-slate-500"
      >
        {{ t('saved_none') }}
      </li>
      <template v-else>
        <li
          v-for="item in items"
          :key="item.id"
          class="flex items-stretch gap-1.5"
        >
          <button
            type="button"
            class="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5 text-left text-xs text-slate-300 transition hover:border-sky-500 hover:text-white"
            @click="open(item.id)"
          >
            {{ labelFor(item) }}
          </button>
          <button
            type="button"
            class="rounded-lg border border-slate-700 bg-slate-950 px-2.5 text-base leading-none text-slate-400 transition hover:border-red-400 hover:text-red-400"
            :aria-label="t('delete')"
            :title="t('delete')"
            @click="remove(item.id)"
          >
            ×
          </button>
        </li>
      </template>
    </ul>
  </div>
</template>
