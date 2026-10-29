<script setup lang="ts">
import { useResumeLibrary } from '~/features/library/composables/useResumeLibrary'
import { formatMatchScore } from '~/shared/utils/score'
import type { JobOut } from '~/shared/schemas/jobs'
import { useJobBoard } from '../composables/useJobBoard'

const { t } = useI18n()
const {
  jobs,
  pending,
  error,
  refresh,
  applications,
  applicationsPending,
  appliedVacancyIds,
  applying,
  apply,
  searchInput,
  applySearch,
  onSearchInput,
  clearSearch
} = useJobBoard()
const { items: resumes, pending: resumesPending } = useResumeLibrary()

const applyOpen = ref(false)
const selectedJob = ref<JobOut | null>(null)
const selectedResumeId = ref<number | undefined>(undefined)

const resumeItems = computed(() =>
  (resumes.value || []).map(item => ({
    label: item.title || item.target_job || `#${item.id}`,
    value: item.id
  }))
)

function openApply(job: JobOut) {
  selectedJob.value = job
  selectedResumeId.value = resumeItems.value[0]?.value
  applyOpen.value = true
}

function closeApply() {
  applyOpen.value = false
  selectedJob.value = null
}

async function confirmApply() {
  if (!selectedJob.value || !selectedResumeId.value) return
  const ok = await apply(selectedJob.value.id, selectedResumeId.value)
  if (ok) closeApply()
}

function vacancyLabel(application: { vacancy_title: string }): string {
  return application.vacancy_title
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
      <h1 class="mb-2 text-3xl font-bold text-slate-100">
        {{ t('jobs_title') }}
      </h1>
      <p class="mb-5 text-slate-400">
        {{ t('jobs_subtitle') }}
      </p>

      <form
        class="mb-6 flex flex-col gap-2 sm:flex-row sm:items-center"
        @submit.prevent="applySearch"
      >
        <UInput
          v-model="searchInput"
          type="search"
          class="w-full flex-1"
          :placeholder="t('jobs_search_placeholder')"
          :aria-label="t('jobs_search_placeholder')"
          @update:model-value="onSearchInput"
        />
        <div class="flex shrink-0 gap-2">
          <UButton
            type="submit"
            color="primary"
            :label="t('jobs_search')"
          />
          <UButton
            type="button"
            color="neutral"
            variant="subtle"
            :label="t('jobs_clear')"
            :disabled="!searchInput"
            @click="clearSearch"
          />
        </div>
      </form>

      <p
        v-if="pending"
        class="text-sm text-slate-500"
      >
        {{ t('jobs_loading') }}
      </p>
      <div
        v-else-if="error"
        class="flex flex-col gap-3"
      >
        <UAlert
          color="error"
          variant="subtle"
          :title="t('load_failed')"
        />
        <UButton
          color="neutral"
          variant="subtle"
          class="self-start"
          :label="t('retry')"
          @click="refresh()"
        />
      </div>
      <p
        v-else-if="!jobs?.length"
        class="text-sm text-slate-500"
      >
        {{ t('jobs_empty') }}
      </p>
      <ul
        v-else
        class="flex list-none flex-col gap-3"
      >
        <li
          v-for="job in jobs"
          :key="job.id"
          class="flex flex-col gap-3 rounded-2xl border border-white/10 bg-slate-950/40 p-4 sm:flex-row sm:items-start sm:justify-between"
        >
          <div>
            <p class="font-semibold text-slate-100">
              {{ job.title }}
            </p>
            <p class="mt-1 text-sm text-sky-400">
              {{ job.company_name }}
            </p>
            <p
              v-if="job.description"
              class="mt-2 text-sm text-slate-400"
            >
              {{ job.description }}
            </p>
          </div>
          <UButton
            v-if="appliedVacancyIds.has(job.id)"
            color="neutral"
            variant="subtle"
            size="sm"
            disabled
            :label="t('jobs_already_applied')"
          />
          <UButton
            v-else
            color="primary"
            size="sm"
            :label="t('jobs_apply')"
            @click="openApply(job)"
          />
        </li>
      </ul>
    </section>

    <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
      <h2 class="mb-4 text-lg font-semibold text-sky-400">
        {{ t('jobs_my_applications') }}
      </h2>
      <p
        v-if="applicationsPending"
        class="text-sm text-slate-500"
      >
        {{ t('jobs_loading') }}
      </p>
      <p
        v-else-if="!applications?.length"
        class="text-sm text-slate-500"
      >
        {{ t('applications_empty') }}
      </p>
      <ul
        v-else
        class="flex list-none flex-col gap-2"
      >
        <li
          v-for="application in applications"
          :key="application.id"
          class="flex flex-wrap items-center justify-between gap-2 rounded-xl border border-white/10 px-4 py-3 text-sm"
        >
          <span class="text-slate-200">
            {{ vacancyLabel(application) }}
          </span>
          <span class="text-sky-400">
            {{ formatMatchScore(application.match_score) }}
          </span>
        </li>
      </ul>
    </section>

    <UModal
      v-model:open="applyOpen"
      :title="t('jobs_apply_title')"
      :ui="{ content: 'sm:max-w-md' }"
    >
      <template #body>
        <p
          v-if="selectedJob"
          class="mb-4 text-sm text-slate-400"
        >
          {{ selectedJob.title }}
        </p>
        <p
          v-if="resumesPending"
          class="text-sm text-slate-500"
        >
          {{ t('saved_loading') }}
        </p>
        <div
          v-else-if="!resumeItems.length"
          class="flex flex-col gap-3"
        >
          <p class="text-sm text-slate-400">
            {{ t('jobs_no_resumes') }}
          </p>
          <UButton
            to="/"
            color="primary"
            :label="t('jobs_go_create')"
            @click="closeApply"
          />
        </div>
        <form
          v-else
          class="flex flex-col gap-4"
          @submit.prevent="confirmApply"
        >
          <UFormField
            :label="t('jobs_pick_resume')"
            name="resume_id"
          >
            <USelect
              v-model="selectedResumeId"
              :items="resumeItems"
              class="w-full"
            />
          </UFormField>
          <div class="flex justify-end gap-2">
            <UButton
              type="button"
              color="neutral"
              variant="subtle"
              :label="t('cancel')"
              @click="closeApply"
            />
            <UButton
              type="submit"
              color="primary"
              :label="t('jobs_apply')"
              :loading="applying"
              :disabled="!selectedResumeId"
            />
          </div>
        </form>
      </template>
    </UModal>
  </div>
</template>
