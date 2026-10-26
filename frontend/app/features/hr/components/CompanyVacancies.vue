<script setup lang="ts">
import type { VacancyOut, VacancyStatus } from '~/shared/schemas/hr'
import { useCompanyVacancies } from '../composables/useCompanyVacancies'

const props = defineProps<{
  companyId: number
}>()

const { t } = useI18n()
const companyId = computed(() => props.companyId)
const {
  company,
  companyPending,
  items,
  pending,
  error,
  refresh,
  create,
  update,
  remove
} = useCompanyVacancies(companyId)

const form = reactive({
  title: '',
  description: '',
  status: 'open' as VacancyStatus
})
const editingId = ref<number | null>(null)
const saving = ref(false)

const statusItems = computed(() => [
  { label: t('vacancies_open'), value: 'open' },
  { label: t('vacancies_closed'), value: 'closed' }
])

const submitLabel = computed(() =>
  editingId.value ? t('save') : t('vacancies_create')
)

function resetForm() {
  form.title = ''
  form.description = ''
  form.status = 'open'
  editingId.value = null
}

function startEdit(vacancy: VacancyOut) {
  editingId.value = vacancy.id
  form.title = vacancy.title
  form.description = vacancy.description || ''
  form.status = vacancy.status
}

function payload() {
  return {
    title: form.title.trim(),
    description: form.description.trim(),
    status: form.status
  }
}

async function onSubmit() {
  if (!form.title.trim()) return
  saving.value = true
  const ok = editingId.value
    ? await update(editingId.value, payload())
    : await create(payload())
  saving.value = false
  if (ok) resetForm()
}

async function onDelete(id: number) {
  await remove(id)
  if (editingId.value === id) resetForm()
}

function applicantsTo(vacancyId: number): string {
  return `/hr/vacancies/${vacancyId}`
}
</script>

<template>
  <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
    <div class="mb-6">
      <UButton
        to="/hr/companies"
        color="neutral"
        variant="ghost"
        class="mb-3 px-0"
        :label="t('back')"
      />
      <h1 class="text-3xl font-bold text-slate-100">
        {{ companyPending ? t('companies_loading') : (company?.name || t('company_not_found')) }}
      </h1>
      <p
        v-if="company?.description"
        class="mt-2 text-slate-400"
      >
        {{ company.description }}
      </p>
    </div>

    <form
      class="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2"
      @submit.prevent="onSubmit"
    >
      <UFormField
        :label="t('vacancies_title_field')"
        name="title"
        required
        class="sm:col-span-2"
      >
        <UInput
          v-model="form.title"
          required
          class="w-full"
        />
      </UFormField>
      <UFormField
        :label="t('description')"
        name="description"
        class="sm:col-span-2"
      >
        <UTextarea
          v-model="form.description"
          class="w-full"
          :rows="3"
        />
      </UFormField>
      <UFormField
        :label="t('vacancies_status')"
        name="status"
      >
        <USelect
          v-model="form.status"
          :items="statusItems"
          class="w-full"
        />
      </UFormField>
      <div class="flex items-end gap-2">
        <UButton
          type="submit"
          color="primary"
          :label="submitLabel"
          :loading="saving"
        />
        <UButton
          v-if="editingId"
          type="button"
          color="neutral"
          variant="subtle"
          :label="t('cancel')"
          @click="resetForm"
        />
      </div>
    </form>

    <h2 class="mb-3 text-lg font-semibold text-sky-400">
      {{ t('vacancies_title') }}
    </h2>

    <p
      v-if="pending"
      class="text-sm text-slate-500"
    >
      {{ t('vacancies_loading') }}
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
      v-else-if="!items?.length"
      class="text-sm text-slate-500"
    >
      {{ t('vacancies_empty') }}
    </p>
    <ul
      v-else
      class="flex list-none flex-col gap-3"
    >
      <li
        v-for="vacancy in items"
        :key="vacancy.id"
        class="flex flex-col gap-3 rounded-2xl border border-white/10 bg-slate-950/40 p-4 sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <p class="font-semibold text-slate-100">
            {{ vacancy.title }}
          </p>
          <p class="mt-1 text-xs tracking-wide text-slate-500 uppercase">
            {{ vacancy.status === 'open' ? t('vacancies_open') : t('vacancies_closed') }}
          </p>
        </div>
        <div class="flex flex-wrap gap-2">
          <UButton
            :to="applicantsTo(vacancy.id)"
            color="primary"
            variant="subtle"
            size="sm"
            :label="t('vacancies_applicants')"
          />
          <UButton
            color="neutral"
            variant="subtle"
            size="sm"
            :label="t('edit')"
            @click="startEdit(vacancy)"
          />
          <UButton
            color="error"
            variant="subtle"
            size="sm"
            :label="t('delete')"
            @click="onDelete(vacancy.id)"
          />
        </div>
      </li>
    </ul>
  </section>
</template>
