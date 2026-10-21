<script setup>
import { computed } from 'vue'
import { scoreBand } from '../scores'

const props = defineProps({
  feedback: { type: Object, required: true },
})

const band = computed(() => scoreBand(props.feedback.overall_score))
</script>

<template>
  <section class="result">
    <div class="card overall">
      <div class="score" :class="band.cls">
        {{ feedback.overall_score }}<span>/100</span>
      </div>
      <div>
        <p class="band" :class="band.cls">{{ band.label }}</p>
        <p>{{ feedback.summary }}</p>
      </div>
    </div>

    <div class="card">
      <h2>Strengths</h2>
      <ul>
        <li v-for="item in feedback.strengths" :key="item">{{ item }}</li>
      </ul>
    </div>

    <div class="card">
      <h2>Weaknesses</h2>
      <ul>
        <li v-for="item in feedback.weaknesses" :key="item">{{ item }}</li>
      </ul>
    </div>

    <div class="card">
      <h2>How to improve your answers</h2>
      <div v-for="item in feedback.answer_improvements" :key="item.question" class="improvement">
        <h3>{{ item.question }}</h3>
        <p><strong>What was weak:</strong> {{ item.issue }}</p>
        <p><strong>How to improve:</strong> {{ item.how_to_improve }}</p>
      </div>
    </div>
  </section>
</template>
