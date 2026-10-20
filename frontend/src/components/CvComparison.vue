<script setup>
import { computed } from 'vue'
import { deltaClass, formatDelta } from '../scores'

const props = defineProps({
  current: { type: Object, required: true },
  previous: { type: Object, required: true },
  previousDate: { type: String, default: '' },
})

const overallDelta = computed(() => props.current.overall_score - props.previous.overall_score)

// One row per section: score now, score before, and the change
const rows = computed(() =>
  props.current.sections.map((section) => {
    // match sections by name, ignoring upper/lower case
    const old = props.previous.sections.find(
      (p) => p.name.toLowerCase() === section.name.toLowerCase(),
    )
    return {
      name: section.name,
      now: section.score,
      before: old ? old.score : null,
      delta: old ? section.score - old.score : null,
    }
  }),
)
</script>

<template>
  <div class="card">
    <h2>Progress since your last review</h2>
    <p class="muted" v-if="previousDate">Compared with {{ new Date(previousDate).toLocaleString() }}</p>

    <p class="overall-delta">
      Overall: {{ previous.overall_score }} &rarr; {{ current.overall_score }}
      <strong :class="deltaClass(overallDelta)">({{ formatDelta(overallDelta) }})</strong>
    </p>

    <table>
      <thead>
        <tr><th>Section</th><th>Before</th><th>Now</th><th>Change</th></tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.name">
          <td class="cap">{{ row.name }}</td>
          <td>{{ row.before ?? '-' }}</td>
          <td>{{ row.now }}</td>
          <td :class="deltaClass(row.delta)">{{ formatDelta(row.delta) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
