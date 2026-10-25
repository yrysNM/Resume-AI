<script setup lang="ts">
import { useAuth } from '../composables/useAuth'

const { t } = useI18n()
const {
  isAuthenticated,
  displayName,
  openModal,
  logout
} = useAuth()

const emit = defineEmits<{
  logout: []
}>()

function onLogout() {
  logout()
  emit('logout')
}
</script>

<template>
  <div class="flex items-center gap-2">
    <template v-if="isAuthenticated">
      <span
        class="max-w-40 truncate text-sm text-slate-400"
        :title="displayName"
      >
        {{ displayName }}
      </span>
      <UButton
        color="neutral"
        variant="subtle"
        size="sm"
        :label="t('logout')"
        @click="onLogout"
      />
    </template>
    <template v-else>
      <UButton
        color="neutral"
        variant="subtle"
        size="sm"
        :label="t('login')"
        @click="openModal('login')"
      />
      <UButton
        color="primary"
        size="sm"
        :label="t('register')"
        @click="openModal('register')"
      />
    </template>
  </div>
</template>
