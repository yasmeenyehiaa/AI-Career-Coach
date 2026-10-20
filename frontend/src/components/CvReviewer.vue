<script setup>
import { computed, ref } from 'vue'
import { reviewCv } from '../api'
import { downloadReviewPdf } from '../pdf'
import { clearHistory, loadHistory, saveHistory } from '../storage'
import CvResult from './CvResult.vue'

// --- form state (ref = a reactive variable; use .value in the script) ---
const role = ref('')
const jobDescription = ref('')
const mode = ref('text') // 'text' = paste, 'file' = upload PDF
const cvText = ref('')
const file = ref(null)

// --- request state ---
const loading = ref(false)
const error = ref('')

// --- saved reviews: loaded from localStorage when the page opens ---
// Each entry looks like: { date, role, review }
const history = ref(loadHistory())

// The latest review is the one we show
const lastEntry = computed(() => history.value.at(-1) || null)

// The review to compare with: the most recent EARLIER review for the same role
const previousEntry = computed(() => {
  const last = lastEntry.value
  if (!last) return null
  const earlier = history.value.slice(0, -1).reverse() // newest first
  return earlier.find((e) => e.role.toLowerCase() === last.role.toLowerCase()) || null
})

// After a refresh, bring the last role back into the form
if (lastEntry.value) role.value = lastEntry.value.role

const MAX_FILE_MB = 4

function onFileChange(event) {
  file.value = event.target.files[0] || null
}

async function submit() {
  error.value = ''

  // Quick checks before calling the server
  if (!role.value.trim()) {
    error.value = 'Please enter the target role.'
    return
  }
  if (mode.value === 'text' && !cvText.value.trim()) {
    error.value = 'Please paste your CV text.'
    return
  }
  if (mode.value === 'file') {
    if (!file.value) {
      error.value = 'Please choose a PDF file.'
      return
    }
    if (file.value.size > MAX_FILE_MB * 1024 * 1024) {
      error.value = `The file is too large (max ${MAX_FILE_MB} MB).`
      return
    }
  }

  loading.value = true
  try {
    const result = await reviewCv({
      role: role.value.trim(),
      jobDescription: jobDescription.value.trim(),
      // send only the chosen input
      cvText: mode.value === 'text' ? cvText.value : '',
      file: mode.value === 'file' ? file.value : null,
    })

    // Add to history and save it (keep only the last 5)
    history.value = [
      ...history.value,
      { date: new Date().toISOString(), role: role.value.trim(), review: result },
    ].slice(-5)
    saveHistory(history.value)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false // runs whether it worked or failed
  }
}

async function downloadPdf() {
  error.value = ''
  try {
    await downloadReviewPdf(
      lastEntry.value.review,
      lastEntry.value.role,
      previousEntry.value ? previousEntry.value.review : null,
    )
  } catch {
    error.value = 'Could not create the PDF. Please try again.'
  }
}

function clearResults() {
  history.value = []
  clearHistory()
}
</script>

<template>
  <form class="card" @submit.prevent="submit">
    <label>
      Target role *
      <input v-model="role" type="text" placeholder="e.g. Junior Data Analyst" />
    </label>

    <label>
      Job description (optional)
      <textarea v-model="jobDescription" rows="4" placeholder="Paste the job offer here..." />
    </label>

    <fieldset>
      <legend>Your CV *</legend>
      <div class="toggle">
        <label><input v-model="mode" type="radio" value="text" /> Paste text</label>
        <label><input v-model="mode" type="radio" value="file" /> Upload PDF</label>
      </div>

      <textarea
        v-if="mode === 'text'"
        v-model="cvText"
        rows="10"
        placeholder="Paste your CV here..."
      />
      <input v-else type="file" accept="application/pdf" @change="onFileChange" />
    </fieldset>

    <p v-if="lastEntry" class="muted">
      Improved your CV? Edit it above and submit again with the same role to see how your score changes.
    </p>

    <p v-if="error" class="error">{{ error }}</p>

    <button type="submit" :disabled="loading">
      {{ loading ? 'Analyzing your CV...' : lastEntry ? 'Review again' : 'Review my CV' }}
    </button>
  </form>

  <template v-if="lastEntry">
    <div class="toolbar">
      <button type="button" class="secondary" @click="downloadPdf">Download PDF</button>
      <button type="button" class="secondary" @click="clearResults">Clear saved results</button>
    </div>

    <CvResult
      :review="lastEntry.review"
      :previous="previousEntry ? previousEntry.review : null"
      :previous-date="previousEntry ? previousEntry.date : ''"
    />
  </template>
</template>
