<script setup lang="ts">
definePageMeta({
  middleware: ['auth', 'hr'],
  layout: 'default'
})
</script>

<template>
  <NuxtPage />
</template>
