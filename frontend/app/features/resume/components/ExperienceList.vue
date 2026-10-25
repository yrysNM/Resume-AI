<script setup lang="ts">
import type { ExperienceItem } from '~/shared/schemas/resume'

const { t } = useI18n()

const experience = defineModel<ExperienceItem[]>('experience', { required: true })

const emit = defineEmits<{
  add: []
  remove: [index: number]
}>()

const canRemove = computed(() => experience.value.length > 1)
</script>

<template>
  <div class="flex flex-col gap-4">
    <div
      v-for="(item, index) in experience"
      :key="index"
      class="rounded-xl border border-slate-700 bg-slate-950 p-4"
    >
      <div class="mb-3 flex items-center justify-between gap-3">
        <span class="text-sm font-semibold text-slate-100">
          {{ t('experience_n') }} {{ index + 1 }}
        </span>
        <UButton
          type="button"
          color="neutral"
          variant="subtle"
          size="sm"
          :label="t('remove_experience')"
          :disabled="!canRemove"
          @click="emit('remove', index)"
        />
      </div>

      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <UFormField :label="t('company')">
          <UInput
            v-model="item.company"
            class="w-full"
          />
        </UFormField>
        <UFormField :label="t('role')">
          <UInput
            v-model="item.role"
            class="w-full"
          />
        </UFormField>
        <UFormField
          class="sm:col-span-2"
          :label="t('period')"
        >
          <UInput
            v-model="item.period"
            class="w-full"
          />
        </UFormField>
        <UFormField
          class="sm:col-span-2"
          :label="t('description')"
        >
          <UTextarea
            v-model="item.description"
            :rows="4"
            class="w-full"
          />
        </UFormField>
      </div>
    </div>

    <div>
      <UButton
        type="button"
        color="neutral"
        variant="subtle"
        size="sm"
        :label="t('add_experience')"
        @click="emit('add')"
      />
    </div>
  </div>
</template>
