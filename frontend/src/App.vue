<script setup>
import { ref } from 'vue'
import CvReviewer from './components/CvReviewer.vue'
import Interviewer from './components/Interviewer.vue'

const tab = ref('cv') // 'cv' or 'interview'
</script>

<template>
  <main class="container">
    <h1>AI Career Coach</h1>
    <p class="subtitle">Improve your CV and practice interviews for the role you want.</p>

    <nav class="tabs">
      <button type="button" :class="{ active: tab === 'cv' }" @click="tab = 'cv'">
        CV Reviewer
      </button>
      <button type="button" :class="{ active: tab === 'interview' }" @click="tab = 'interview'">
        Mock Interview
      </button>
    </nav>

    <!-- v-show hides a tab instead of destroying it, so nothing is lost when you switch -->
    <div v-show="tab === 'cv'"><CvReviewer /></div>  
    <div v-show="tab === 'interview'"><Interviewer /></div>
  </main>
</template>