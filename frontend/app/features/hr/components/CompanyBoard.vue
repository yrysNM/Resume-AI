<script setup lang="ts">
import type { CompanyOut } from '~/shared/schemas/hr'
import { useCompanies } from '../composables/useCompanies'

const { t } = useI18n()
const { items, pending, error, refresh, create, update, remove } = useCompanies()

const form = reactive({
  name: '',
  description: '',
  website: ''
})
const editingId = ref<number | null>(null)
const saving = ref(false)

const submitLabel = computed(() =>
  editingId.value ? t('save') : t('companies_create')
)

function resetForm() {
  form.name = ''
  form.description = ''
  form.website = ''
  editingId.value = null
}

function startEdit(company: CompanyOut) {
  editingId.value = company.id
  form.name = company.name
  form.description = company.description || ''
  form.website = company.website || ''
}

function payload() {
  return {
    name: form.name.trim(),
    description: form.description.trim(),
    website: form.website.trim() || null
  }
}

async function onSubmit() {
  if (!form.name.trim()) return
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
</script>

<template>
  <section class="rounded-2xl border border-white/10 bg-white/5 p-5 sm:p-8">
    <h1 class="mb-2 text-3xl font-bold text-slate-100">
      {{ t('companies_title') }}
    </h1>
    <p class="mb-7 text-slate-400">
      {{ t('companies_subtitle') }}
    </p>

    <form
      class="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2"
      @submit.prevent="onSubmit"
    >
      <UFormField
        :label="t('companies_name')"
        name="name"
        required
        class="sm:col-span-2"
      >
        <UInput
          v-model="form.name"
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
        :label="t('companies_website')"
        name="website"
      >
        <UInput
          v-model="form.website"
          type="url"
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

    <p
      v-if="pending"
      class="text-sm text-slate-500"
    >
      {{ t('companies_loading') }}
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
      {{ t('companies_empty') }}
    </p>
    <ul
      v-else
      class="flex list-none flex-col gap-3"
    >
      <li
        v-for="company in items"
        :key="company.id"
        class="flex flex-col gap-3 rounded-2xl border border-white/10 bg-slate-950/40 p-4 sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <p class="font-semibold text-slate-100">
            {{ company.name }}
          </p>
          <p
            v-if="company.description"
            class="mt-1 text-sm text-slate-400"
          >
            {{ company.description }}
          </p>
        </div>
        <div class="flex flex-wrap gap-2">
          <UButton
            :to="`/hr/companies/${company.id}`"
            color="primary"
            variant="subtle"
            size="sm"
            :label="t('companies_open')"
          />
          <UButton
            color="neutral"
            variant="subtle"
            size="sm"
            :label="t('edit')"
            @click="startEdit(company)"
          />
          <UButton
            color="error"
            variant="subtle"
            size="sm"
            :label="t('delete')"
            @click="onDelete(company.id)"
          />
        </div>
      </li>
    </ul>
  </section>
</template>
