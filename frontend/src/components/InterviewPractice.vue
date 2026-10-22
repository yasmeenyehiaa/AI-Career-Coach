<script setup>
import { ref } from 'vue'
import AnswerCoach from './AnswerCoach.vue'
import Interviewer from './Interviewer.vue'

const mode = ref('full')
</script>

<template>
  <section>
    <div class="practice-nav-wrap">
      <nav class="tabs practice-tabs" aria-label="Interview practice mode">
        <button type="button" :class="{ active: mode === 'full' }" @click="mode = 'full'">
          Full Mock Interview
        </button>
        <button type="button" :class="{ active: mode === 'single' }" @click="mode = 'single'">
          Practice One Question
        </button>
      </nav>
    </div>

    <div v-show="mode === 'full'"><Interviewer /></div>
    <div v-show="mode === 'single'"><AnswerCoach /></div>
  </section>
</template>
