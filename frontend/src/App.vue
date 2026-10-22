<script setup>
import { ref } from 'vue'
import CvReviewer from './components/CvReviewer.vue'
import InterviewPractice from './components/InterviewPractice.vue'

const tab = ref('cv')
</script>

<template>
  <main class="container">
    <header class="hero">
      <div class="hero-copy">
        <p class="eyebrow">YOUR NEXT CAREER MOVE STARTS HERE</p>
        <h1>Make your next move with confidence.</h1>
        <p class="subtitle">Get thoughtful CV feedback and practice interviews with your personal AI career coach.</p>
        <div class="hero-highlights" aria-label="Career coaching tools">
          <span>CV feedback</span>
          <span>Interview practice</span>
        </div>
      </div>
      <div class="hero-art">
        <img
          class="hero-image"
          src="/image.png"
          alt="A person using a laptop beside an AI career-coaching dashboard"
        />
      </div>
    </header>

    <nav class="tabs main-tabs">
      <button type="button" :class="{ active: tab === 'cv' }" @click="tab = 'cv'">
        📄 CV Reviewer
      </button>
      <button type="button" :class="{ active: tab === 'interview' }" @click="tab = 'interview'">
        🎤 Interview Practice
      </button>
    </nav>

    <div v-show="tab === 'cv'"><CvReviewer /></div>
    <div v-show="tab === 'interview'"><InterviewPractice /></div>
  </main>
</template>