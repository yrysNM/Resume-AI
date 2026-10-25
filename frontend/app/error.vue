<script setup lang="ts">
import type { NuxtError } from '#app'

defineProps<{
  error: NuxtError
}>()

const handleError = () => clearError({ redirect: '/' })
</script>

<template>
  <UApp>
    <div class="flex min-h-screen flex-col items-center justify-center gap-4 px-6 text-center">
      <h1 class="text-3xl font-bold text-slate-100">
        {{ error.statusCode || 500 }}
      </h1>
      <p class="max-w-md text-slate-400">
        {{ error.statusMessage || error.message || 'Something went wrong' }}
      </p>
      <UButton
        color="primary"
        label="Go home"
        @click="handleError"
      />
    </div>
  </UApp>
</template>
