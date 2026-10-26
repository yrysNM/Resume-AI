<script setup lang="ts">
import type { ResumeLanguage, ResumeTemplate } from '~/shared/schemas/resume'
import { headingsFor, parseResumeText } from '../lib/parseResume'

const props = defineProps<{
  text: string
  template: ResumeTemplate
  language: ResumeLanguage
  placeholder: string
}>()

const parsed = computed(() => parseResumeText(props.text))
const headings = computed(() => headingsFor(props.language))
const empty = computed(() => !props.text.trim())
</script>

<template>
  <article
    class="min-h-70 overflow-hidden rounded-lg"
    :class="{
      'bg-[#faf8f5] p-7 font-serif text-slate-900': template === 'classic',
      'bg-white font-sans text-slate-900': template === 'modern',
      'bg-white p-9 font-sans text-slate-800': template === 'minimal'
    }"
  >
    <p
      v-if="empty"
      class="text-sm text-slate-400"
    >
      {{ placeholder }}
    </p>

    <template v-else-if="template === 'classic'">
      <h2 class="text-2xl font-bold">
        {{ parsed.name || parsed.raw.split('\n')[0] }}
      </h2>
      <p
        v-if="parsed.headline"
        class="mt-1 text-sm text-slate-600"
      >
        {{ parsed.headline }}
      </p>
      <template v-if="parsed.hasSections">
        <section
          v-if="parsed.target"
          class="mt-5"
        >
          <h3 class="border-b border-slate-800 pb-1 text-xs font-bold tracking-wide uppercase">
            {{ headings.target }}
          </h3>
          <p class="mt-2 text-sm whitespace-pre-wrap">
            {{ parsed.target }}
          </p>
        </section>
        <section
          v-if="parsed.experience"
          class="mt-5"
        >
          <h3 class="border-b border-slate-800 pb-1 text-xs font-bold tracking-wide uppercase">
            {{ headings.experience }}
          </h3>
          <p class="mt-2 text-sm whitespace-pre-wrap">
            {{ parsed.experience }}
          </p>
        </section>
        <section
          v-if="parsed.skills"
          class="mt-5"
        >
          <h3 class="border-b border-slate-800 pb-1 text-xs font-bold tracking-wide uppercase">
            {{ headings.skills }}
          </h3>
          <p class="mt-2 text-sm whitespace-pre-wrap">
            {{ parsed.skills }}
          </p>
        </section>
        <section
          v-if="parsed.education"
          class="mt-5"
        >
          <h3 class="border-b border-slate-800 pb-1 text-xs font-bold tracking-wide uppercase">
            {{ headings.education }}
          </h3>
          <p class="mt-2 text-sm whitespace-pre-wrap">
            {{ parsed.education }}
          </p>
        </section>
      </template>
      <p
        v-else
        class="mt-4 text-sm leading-relaxed whitespace-pre-wrap"
      >
        {{ parsed.raw }}
      </p>
    </template>

    <template v-else-if="template === 'modern'">
      <header class="bg-sky-600 px-6 py-5 text-white">
        <h2 class="text-2xl font-bold">
          {{ parsed.name || parsed.raw.split('\n')[0] }}
        </h2>
        <p
          v-if="parsed.headline"
          class="mt-1 text-sm text-sky-50"
        >
          {{ parsed.headline }}
        </p>
      </header>
      <div
        v-if="parsed.hasSections"
        class="grid grid-cols-1 gap-6 p-6 sm:grid-cols-[minmax(0,0.38fr)_minmax(0,0.62fr)]"
      >
        <aside class="space-y-5">
          <section v-if="parsed.skills">
            <h3 class="text-xs font-bold tracking-widest text-sky-600 uppercase">
              {{ headings.skills }}
            </h3>
            <p class="mt-2 text-sm whitespace-pre-wrap">
              {{ parsed.skills }}
            </p>
          </section>
          <section v-if="parsed.education">
            <h3 class="text-xs font-bold tracking-widest text-sky-600 uppercase">
              {{ headings.education }}
            </h3>
            <p class="mt-2 text-sm whitespace-pre-wrap">
              {{ parsed.education }}
            </p>
          </section>
        </aside>
        <div class="space-y-5">
          <section v-if="parsed.target">
            <h3 class="text-xs font-bold tracking-widest text-sky-600 uppercase">
              {{ headings.target }}
            </h3>
            <p class="mt-2 text-sm whitespace-pre-wrap">
              {{ parsed.target }}
            </p>
          </section>
          <section v-if="parsed.experience">
            <h3 class="text-xs font-bold tracking-widest text-sky-600 uppercase">
              {{ headings.experience }}
            </h3>
            <p class="mt-2 text-sm whitespace-pre-wrap">
              {{ parsed.experience }}
            </p>
          </section>
        </div>
      </div>
      <p
        v-else
        class="p-6 text-sm leading-relaxed whitespace-pre-wrap"
      >
        {{ parsed.raw }}
      </p>
    </template>

    <template v-else>
      <h2 class="text-3xl font-light tracking-tight">
        {{ parsed.name || parsed.raw.split('\n')[0] }}
      </h2>
      <p
        v-if="parsed.headline"
        class="mt-2 text-xs tracking-[0.18em] text-slate-500 uppercase"
      >
        {{ parsed.headline }}
      </p>
      <template v-if="parsed.hasSections">
        <section
          v-if="parsed.target"
          class="mt-8"
        >
          <h3 class="text-[11px] font-medium tracking-[0.22em] text-slate-400 uppercase">
            {{ headings.target }}
          </h3>
          <div class="mt-2 h-px bg-slate-200" />
          <p class="mt-3 text-sm leading-7 whitespace-pre-wrap">
            {{ parsed.target }}
          </p>
        </section>
        <section
          v-if="parsed.experience"
          class="mt-8"
        >
          <h3 class="text-[11px] font-medium tracking-[0.22em] text-slate-400 uppercase">
            {{ headings.experience }}
          </h3>
          <div class="mt-2 h-px bg-slate-200" />
          <p class="mt-3 text-sm leading-7 whitespace-pre-wrap">
            {{ parsed.experience }}
          </p>
        </section>
        <section
          v-if="parsed.skills"
          class="mt-8"
        >
          <h3 class="text-[11px] font-medium tracking-[0.22em] text-slate-400 uppercase">
            {{ headings.skills }}
          </h3>
          <div class="mt-2 h-px bg-slate-200" />
          <p class="mt-3 text-sm leading-7 whitespace-pre-wrap">
            {{ parsed.skills }}
          </p>
        </section>
        <section
          v-if="parsed.education"
          class="mt-8"
        >
          <h3 class="text-[11px] font-medium tracking-[0.22em] text-slate-400 uppercase">
            {{ headings.education }}
          </h3>
          <div class="mt-2 h-px bg-slate-200" />
          <p class="mt-3 text-sm leading-7 whitespace-pre-wrap">
            {{ parsed.education }}
          </p>
        </section>
      </template>
      <p
        v-else
        class="mt-6 text-sm leading-7 whitespace-pre-wrap"
      >
        {{ parsed.raw }}
      </p>
    </template>
  </article>
</template>
