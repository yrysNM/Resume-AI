<script setup lang="ts">
import type { UserRole } from '~/shared/schemas/auth'
import { useAuth } from '../composables/useAuth'

const { t } = useI18n()
const {
  modalOpen,
  authMode,
  authError,
  pending,
  isHr,
  closeModal,
  submitAuth
} = useAuth()

const form = reactive({
  full_name: '',
  email: '',
  password: '',
  role: 'seeker' as UserRole
})

const roleItems = computed(() => [
  { label: t('role_seeker'), value: 'seeker' },
  { label: t('role_hr'), value: 'hr' }
])

watch(modalOpen, (open) => {
  if (open) {
    form.full_name = ''
    form.email = ''
    form.password = ''
    form.role = 'seeker'
  }
})

const title = computed(() =>
  authMode.value === 'register' ? t('register') : t('login')
)

async function onSubmit() {
  const registering = authMode.value === 'register'
  const ok = await submitAuth({
    email: form.email.trim(),
    password: form.password,
    full_name: form.full_name.trim(),
    role: form.role
  })
  if (!ok) return
  form.full_name = ''
  form.email = ''
  form.password = ''
  form.role = 'seeker'
  if (isHr.value) {
    await navigateTo('/hr')
  } else if (registering) {
    await navigateTo('/')
  }
}
</script>

<template>
  <UModal
    v-model:open="modalOpen"
    :title="title"
    :ui="{ content: 'sm:max-w-md' }"
  >
    <template #body>
      <form
        class="flex flex-col gap-4"
        @submit.prevent="onSubmit"
      >
        <UFormField
          v-if="authMode === 'register'"
          :label="t('full_name')"
          name="full_name"
        >
          <UInput
            v-model="form.full_name"
            autocomplete="name"
            class="w-full"
          />
        </UFormField>

        <UFormField
          :label="t('email')"
          name="email"
          required
        >
          <UInput
            v-model="form.email"
            type="email"
            required
            autocomplete="email"
            class="w-full"
          />
        </UFormField>

        <UFormField
          :label="t('password')"
          name="password"
          required
        >
          <UInput
            v-model="form.password"
            type="password"
            required
            minlength="8"
            :autocomplete="authMode === 'register' ? 'new-password' : 'current-password'"
            class="w-full"
          />
        </UFormField>

        <UFormField
          v-if="authMode === 'register'"
          :label="t('role_label')"
          name="role"
        >
          <URadioGroup
            v-model="form.role"
            :items="roleItems"
          />
        </UFormField>

        <UAlert
          v-if="authError"
          color="error"
          variant="subtle"
          :title="authError"
        />

        <div class="flex justify-end gap-2 pt-2">
          <UButton
            type="button"
            color="neutral"
            variant="subtle"
            :label="t('cancel')"
            @click="closeModal()"
          />
          <UButton
            type="submit"
            color="primary"
            :label="title"
            :loading="pending"
          />
        </div>
      </form>
    </template>
  </UModal>
</template>
