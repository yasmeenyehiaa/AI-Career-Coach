<script setup>
import { computed } from 'vue'
import { scoreBand } from '../scores.js'

const props = defineProps({
  review: { type: Object, required: true },
})

const overallBand = computed(() => scoreBand(props.review.overall_score))
</script>

<template>
  <section class="result">
    <div class="card overall">
      <div class="score" :class="overallBand.cls">
        {{ review.overall_score }}<span>/100</span>
      </div>
      <div>
        <p class="band" :class="overallBand.cls">{{ overallBand.label }}</p>
        <p>{{ review.summary }}</p>
      </div>
    </div>

    <div class="card">
      <h2>Top priorities</h2>
      <ol>
        <li v-for="item in review.top_priorities" :key="item">{{ item }}</li>
      </ol>
    </div>

    <div v-if="review.missing_skills.length" class="card">
      <h2>Missing skills</h2>
      <div class="chips">
        <span v-for="skill in review.missing_skills" :key="skill" class="chip">{{ skill }}</span>
      </div>
    </div>

    <div v-for="section in review.sections" :key="section.name" class="card">
      <h2>
        {{ section.name }}
        <span class="badge" :class="scoreBand(section.score).cls">
          {{ scoreBand(section.score).label }} &middot; {{ section.score }}
        </span>
      </h2>

      <h3>Strengths</h3>
      <ul>
        <li v-for="s in section.strengths" :key="s">{{ s }}</li>
      </ul>

      <h3>Suggestions</h3>
      <ul>
        <li v-for="s in section.suggestions" :key="s">{{ s }}</li>
      </ul>
    </div>
  </section>
</template>
