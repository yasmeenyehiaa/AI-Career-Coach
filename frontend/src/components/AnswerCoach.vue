<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { analyzeAnswer, generateQuestion, getCategories } from '../api'
import { deltaClass, formatDelta, scoreBand } from '../scores'

const STAR_ORDER = ['Situation', 'Task', 'Action', 'Result']

const STATUS = {
  strong: { label: 'Strong', cls: 'good' },
  partial: { label: 'Needs work', cls: 'ok' },
  missing: { label: 'Missing', cls: 'bad' },
}

const role = ref('')
const question = ref('')
const answer = ref('')
const category = ref('')   
const categories = ref([]) 
const showQuestionGenerator = ref(false)

const generating = ref(false)
const analyzing = ref(false)
const error = ref('')

const analysis = ref(null)
const analyzedQuestion = ref('')   
const previousScore = ref(null)    
const parts = ref({})              
const activeName = ref('Situation') 
const resultsTop = ref(null)

const band = computed(() => (analysis.value ? scoreBand(analysis.value.score) : null))
const scoreDelta = computed(() =>
  analysis.value && previousScore.value !== null ? analysis.value.score - previousScore.value : null,
)
const activeComponent = computed(
  () => analysis.value?.components.find((c) => c.name === activeName.value) || null,
)
const activeIndex = computed(() =>
  analysis.value ? analysis.value.components.findIndex((c) => c.name === activeName.value) : -1,
)

// Load the list of themes when the tab opens
onMounted(async () => {
  try {
    categories.value = (await getCategories()).categories
  } catch {
    // not critical: the dropdown just stays on "Any theme"
  }
})

// "learning from a failure" -> "Learning from a failure"
const label = (text) => text.charAt(0).toUpperCase() + text.slice(1)

// ---- get a random question ----
async function newQuestion() {
  error.value = ''
  generating.value = true
  try {
    const result = await generateQuestion(
      role.value.trim() || null,
      category.value || null,
    )
    question.value = result.question
    showQuestionGenerator.value = false
    // The old analysis belongs to the old question. (The draft answer stays, so nothing is lost.)
    analysis.value = null
    previousScore.value = null
  } catch (e) {
    error.value = e.message
  } finally {
    generating.value = false
  }
}

// ---- analyze the draft ----
async function analyze() {
  error.value = ''
  if (question.value.trim().length < 5) {
    error.value = 'Please paste an interview question, or generate one.'
    return
  }
  if (answer.value.trim().length < 10) {
    error.value = 'Please write a draft answer first (at least a sentence).'
    return
  }

  analyzing.value = true
  analysis.value = null
  previousScore.value = null

  try {
    const result = await analyzeAnswer({
      question: question.value.trim(),
      answer: answer.value.trim(),
      role: role.value.trim() || null,
    })

    // Remember the old score only if it was the same question (so we can show progress)
    const sameQuestion = analyzedQuestion.value === question.value.trim()
    previousScore.value = analysis.value && sameQuestion ? analysis.value.score : null

    analysis.value = result
    analyzedQuestion.value = question.value.trim()

    // Pre-fill each part with the sentences the AI found in the draft, ready to be improved
    parts.value = Object.fromEntries(result.components.map((c) => [c.name, c.found_text]))
    activeName.value = result.start_with // start with the weakest part

    await nextTick()
    resultsTop.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  } catch (e) {
    error.value = e.message
  } finally {
    analyzing.value = false
  }
}

// move between STAR steps
function go(step) {
  const list = analysis.value.components
  const index = activeIndex.value + step
  if (index >= 0 && index < list.length) activeName.value = list[index].name
}

// build a new draft from the four parts, then analyze it again 
async function applyParts() {
  const combined = STAR_ORDER.map((name) => (parts.value[name] || '').trim())
    .filter(Boolean)
    .join('\n\n')
  if (combined.length < 10) {
    error.value = 'Write at least a few words in one of the parts first.'
    return
  }
  answer.value = combined
  await analyze()
}
</script>

<template>
  <form class="card" @submit.prevent="analyze">
    <label>
      Target role
      <input v-model="role" type="text" placeholder="e.g. Junior Data Analyst" />
    </label>

    <label>
      Interview question *
      <textarea
        v-model="question"
        rows="1"
        placeholder="Paste an interview question, e.g. Tell me about a time you disagreed with a teammate..."
      />
    </label>
    <button
      type="button"
      class="secondary"
      :disabled="generating"
      @click="showQuestionGenerator = !showQuestionGenerator"
    >
      {{ showQuestionGenerator ? 'Hide question options' : 'Generate a random question' }}
    </button>

    <div v-if="showQuestionGenerator" class="spaced">
      <label>
        Theme for a random question (optional)
        <select v-model="category">
          <option value="">Any theme (random)</option>
          <option v-for="c in categories" :key="c" :value="c">{{ label(c) }}</option>
        </select>
      </label>
      <button type="button" :disabled="generating" @click="newQuestion">
        {{ generating ? 'Generating...' : 'Generate question' }}
      </button>
    </div>

    <template v-if="question.trim()">
      <label class="spaced">
        Your draft answer *
        <textarea v-model="answer" rows="3" placeholder="Write or paste your answer..." />
      </label>

      <p v-if="error" class="error">{{ error }}</p>

      <button type="submit" :disabled="analyzing">
        {{ analyzing ? 'Analyzing your answer...' : analysis ? 'Analyze again' : 'Analyze my answer' }}
      </button>
    </template>
    <p v-else-if="error" class="error">{{ error }}</p>
  </form>

  <section v-if="analysis && !analyzing" ref="resultsTop" class="result">
    <div class="card overall">
      <div class="score" :class="band.cls">{{ analysis.score }}<span>/100</span></div>
      <div>
        <p class="band" :class="band.cls">
          {{ band.label }}
          <span v-if="scoreDelta !== null" class="delta" :class="deltaClass(scoreDelta)">
            {{ formatDelta(scoreDelta) }} since your last try
          </span>
        </p>
        <p>{{ analysis.summary }}</p>
      </div>
    </div>

    <div class="card">
      <h2>Improve it step by step</h2>
      <p class="muted">
        Work through the four STAR parts. Start with <strong>{{ analysis.start_with }}</strong>, your weakest part.
      </p>

      <div class="steps">
        <button
          v-for="c in analysis.components"
          :key="c.name"
          type="button"
          class="step"
          :class="{ active: c.name === activeName }"
          :aria-pressed="c.name === activeName"
          @click="activeName = c.name"
        >
          {{ c.name }}
          <span class="pill" :class="STATUS[c.status].cls">{{ STATUS[c.status].label }}</span>
        </button>
      </div>

      <div v-if="activeComponent" class="step-panel">
        <h3>What I found in your answer</h3>
        <p v-if="activeComponent.found_text" class="quote">{{ activeComponent.found_text }}</p>
        <p v-else class="muted">Nothing about this part yet.</p>

        <h3>What's missing</h3>
        <p>{{ activeComponent.whats_missing }}</p>

        <h3>Why it matters</h3>
        <p>{{ activeComponent.why_it_matters }}</p>

        <h3>How to improve it</h3>
        <p>{{ activeComponent.how_to_improve }}</p>

        <h3>Questions to help you</h3>
        <ul>
          <li v-for="q in activeComponent.guiding_questions" :key="q">{{ q }}</li>
        </ul>

        <label class="spaced">
          Write your improved {{ activeComponent.name }}
          <textarea v-model="parts[activeComponent.name]" rows="4" placeholder="Answer the questions above in your own words..." />
        </label>

        <div class="row">
          <button type="button" class="secondary" :disabled="activeIndex <= 0" @click="go(-1)">Back</button>
          <button
            type="button"
            class="secondary"
            :disabled="activeIndex >= analysis.components.length - 1"
            @click="go(1)"
          >
            Next part
          </button>
        </div>
      </div>

      <p class="muted spaced">When you are happy with your parts, build a new draft and see how the score changes.</p>
      <button type="button" :disabled="analyzing" @click="applyParts">
        {{ analyzing ? 'Analyzing...' : 'Use these parts as my new draft & analyze again' }}
      </button>
    </div>

    <div v-if="analysis.extra_tips.length" class="card">
      <h2>Extra tips</h2>
      <ul>
        <li v-for="tip in analysis.extra_tips" :key="tip">{{ tip }}</li>
      </ul>
    </div>
  </section>
</template>
