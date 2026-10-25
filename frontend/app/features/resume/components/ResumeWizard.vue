<script setup lang="ts">
import ExperienceList from './ExperienceList.vue'
import AnalysisPanel from './AnalysisPanel.vue'
import ResumePreview from './ResumePreview.vue'
import { useResumeGenerate } from '../composables/useResumeGenerate'
import { useResumeWizard } from '../composables/useResumeWizard'

const emit = defineEmits<{
  generated: []
}>()

const { t } = useI18n()
const {
  step,
  form,
  skillTags,
  next,
  prev,
  addExperience,
  removeExperience
} = useResumeWizard()

const { pending, generate } = useResumeGenerate(async () => {
  emit('generated')
})

async function onGenerate() {
  await generate()
}
</script>

<template>
  <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
    <h1 class="mb-2 text-3xl font-bold text-slate-100">
      {{ t('title') }}
    </h1>
    <p class="mb-7 text-slate-400">
      {{ t('subtitle') }}
    </p>

    <slot name="auth-hint" />

    <form
      class="flex flex-col"
      @submit.prevent
    >
      <!-- Step 1: Personal -->
      <div v-show="step === 1">
        <h3 class="mb-5 text-lg font-semibold text-sky-400">
          {{ t('panel1') }}
        </h3>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <UFormField :label="t('full_name')">
            <UInput
              v-model="form.full_name"
              required
              class="w-full"
            />
          </UFormField>
          <UFormField :label="t('email')">
            <UInput
              v-model="form.email"
              type="email"
              required
              class="w-full"
            />
          </UFormField>
          <UFormField :label="t('phone')">
            <UInput
              v-model="form.phone"
              required
              class="w-full"
            />
          </UFormField>
          <UFormField :label="t('position')">
            <UInput
              v-model="form.position"
              required
              class="w-full"
            />
          </UFormField>
          <UFormField
            class="sm:col-span-2"
            :label="t('target_job')"
          >
            <UInput
              v-model="form.target_job"
              class="w-full"
            />
          </UFormField>
          <UFormField
            class="sm:col-span-2"
            :label="t('education')"
          >
            <UInput
              v-model="form.education"
              class="w-full"
            />
          </UFormField>
        </div>
      </div>

      <!-- Step 2: Experience -->
      <div v-show="step === 2">
        <h3 class="mb-5 text-lg font-semibold text-sky-400">
          {{ t('panel2') }}
        </h3>
        <ExperienceList
          v-model:experience="form.experience"
          @add="addExperience()"
          @remove="removeExperience"
        />
      </div>

      <!-- Step 3: Skills -->
      <div v-show="step === 3">
        <h3 class="mb-5 text-lg font-semibold text-sky-400">
          {{ t('panel3') }}
        </h3>
        <UInput
          v-model="form.skillsText"
          :placeholder="t('skills_placeholder')"
          class="w-full"
        />
        <div class="mt-3 flex flex-wrap gap-2">
          <UBadge
            v-for="tag in skillTags"
            :key="tag"
            color="primary"
            variant="subtle"
            size="md"
          >
            {{ tag }}
          </UBadge>
        </div>
      </div>

      <!-- Step 4: Preview -->
      <div
        v-show="step === 4"
        id="analysis"
      >
        <h3 class="mb-5 text-lg font-semibold text-sky-400">
          {{ t('panel4') }}
        </h3>
        <div class="grid grid-cols-1 gap-5 lg:grid-cols-2">
          <ResumePreview />
          <AnalysisPanel />
        </div>
      </div>

      <div class="mt-7 flex justify-end gap-3">
        <UButton
          type="button"
          color="neutral"
          variant="subtle"
          :label="t('prev')"
          :disabled="step === 1"
          @click="prev"
        />
        <UButton
          v-if="step < 4"
          type="button"
          color="primary"
          :label="t('next')"
          @click="next"
        />
        <UButton
          v-else
          type="button"
          color="success"
          :label="pending ? t('generating') : t('generate')"
          :loading="pending"
          @click="onGenerate"
        />
      </div>
    </form>
  </section>
</template>
