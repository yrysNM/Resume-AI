<script setup lang="ts">
import ResumeDocument from './ResumeDocument.vue'
import { useResumeExport } from '../composables/useResumeExport'
import { useResumeResult } from '../composables/useResumeResult'
import { useResumeWizard } from '../composables/useResumeWizard'
import type { ResumeLanguage, ResumeTemplate } from '~/shared/schemas/resume'

const { t } = useI18n()
const { result } = useResumeResult()
const { form } = useResumeWizard()
const { pending, hasExportable, exportFormat } = useResumeExport()

const previewText = computed(() => result.value?.gen?.resume_text || '')
const generatedBy = computed(() => result.value?.gen?.generated_by || '')
const previewLanguage = computed<ResumeLanguage>(() =>
  result.value?.gen?.language || form.value.language
)
const previewTemplate = computed<ResumeTemplate>(() => form.value.template)
</script>

<template>
  <div class="flex min-h-70 flex-col rounded-xl border border-slate-700 bg-slate-950 p-5">
    <h4 class="mb-3 text-xs font-semibold tracking-wide text-slate-500 uppercase">
      {{ t('resume_box') }}
    </h4>

    <ResumeDocument
      :text="previewText"
      :template="previewTemplate"
      :language="previewLanguage"
      :placeholder="t('placeholder')"
    />

    <div class="mt-4 flex flex-wrap gap-2">
      <UButton
        type="button"
        color="neutral"
        variant="subtle"
        size="sm"
        :label="t('export_pdf')"
        :disabled="!hasExportable"
        :loading="pending"
        @click="exportFormat('pdf')"
      />
      <UButton
        type="button"
        color="neutral"
        variant="subtle"
        size="sm"
        :label="t('export_docx')"
        :disabled="!hasExportable"
        :loading="pending"
        @click="exportFormat('docx')"
      />
    </div>

    <p
      v-if="generatedBy"
      class="mt-3 text-xs break-words text-slate-500"
    >
      {{ t('generated_by') }}: {{ generatedBy }}
    </p>
  </div>
</template>
