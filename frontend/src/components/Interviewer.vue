<script setup>
import { computed, nextTick, ref } from 'vue'
import { getInterviewFeedback, sendAnswer, startInterview } from '../api.js'
import InterviewFeedback from './InterviewFeedback.vue'

const phase = ref('setup')
const role = ref('')
const jobDescription = ref('')
const numQuestions = ref(6)
const messages = ref([]) // [{ role: 'assistant' | 'user', content }]
const answer = ref('')
const loading = ref(false)
const error = ref('')
const feedback = ref(null)
const chatEnd = ref(null) // an empty element at the bottom of the chat, used for scrolling


const setup = computed(() => ({
  role: role.value.trim(),
  job_description: jobDescription.value.trim() || null,
  num_questions: numQuestions.value,
}))


const questionNumber = computed(() => messages.value.filter((m) => m.role === 'assistant').length)
const hasAnswers = computed(() => messages.value.some((m) => m.role === 'user'))

async function scrollToBottom() {
  await nextTick() // wait until Vue has drawn the new message
  chatEnd.value?.scrollIntoView({ behavior: 'smooth', block: 'end' })
}

async function start() {
  error.value = ''
  if (!role.value.trim()) {
    error.value = 'Please enter the role you are preparing for.'
    return
  }

  loading.value = true
  try {
    const { question } = await startInterview(setup.value)
    messages.value = [{ role: 'assistant', content: question }]
    feedback.value = null
    phase.value = 'chat'
    scrollToBottom()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function send() {
  const text = answer.value.trim()
  if (!text || loading.value) return

  error.value = ''
  messages.value.push({ role: 'user', content: text })
  answer.value = ''
  loading.value = true
  scrollToBottom()

  let finished = false
  try {
    const result = await sendAnswer(setup.value, messages.value)
    if (result.finished) {
      finished = true
    } else {
      messages.value.push({ role: 'assistant', content: result.question })
      scrollToBottom()
    }
  } catch (e) {
    // Undo: remove the answer from the chat and put the text back, so nothing is lost
    messages.value.pop()
    answer.value = text
    error.value = e.message
  } finally {
    loading.value = false
  }

  if (finished) finish()
}

async function finish() {
  phase.value = 'feedback'
  feedback.value = null
  error.value = ''
  loading.value = true
  try {
    feedback.value = await getInterviewFeedback(setup.value, messages.value)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function restart() {
  phase.value = 'setup'
  messages.value = []
  answer.value = ''
  feedback.value = null
  error.value = ''
}
</script>

<template>
  <!-- ============ PHASE 1: setup ============ -->
  <form v-if="phase === 'setup'" class="card" @submit.prevent="start">
    <label>
      Role you are preparing for *
      <input v-model="role" type="text" placeholder="e.g. Junior Data Analyst" />
    </label>

    <label>
      Job description (optional)
      <textarea
        v-model="jobDescription"
        rows="5"
        placeholder="Paste the job description to get questions tailored to it..."
      />
    </label>

    <label>
      Number of questions
      <select v-model.number="numQuestions">
        <option :value="1">1 (short)</option> // TODO: remove after testing
        <option :value="4">4 (short)</option>
        <option :value="6">6 (standard)</option>
        <option :value="8">8 (long)</option>
      </select>
    </label>

    <p v-if="error" class="error">{{ error }}</p>

    <button type="submit" :disabled="loading">
      {{ loading ? 'Preparing your interviewer...' : '🎯 Start interview' }}
    </button>
  </form>

  <!-- ============ PHASE 2: the interview ============ -->
  <template v-else-if="phase === 'chat'">
    <div class="chat-header">
      <strong>Question {{ questionNumber }} of {{ numQuestions }}</strong>
      <button
        type="button"
        class="secondary"
        :disabled="loading || !hasAnswers"
        @click="finish"
      >
        ✅ Finish now &amp; get feedback
      </button>
    </div>

    <div class="chat">
      <div v-for="(message, index) in messages" :key="index" class="bubble" :class="message.role">
        <span class="who">{{ message.role === 'assistant' ? 'Interviewer' : 'You' }}</span>
        <p>{{ message.content }}</p>
      </div>
      <div v-if="loading" class="bubble assistant">
        <span class="who">Interviewer</span>
        <p class="muted">is typing...</p>
      </div>
      <div ref="chatEnd"></div>
    </div>

    <div class="answer-box">
      <textarea
        v-model="answer"
        rows="4"
        placeholder="Type your answer..."
        :disabled="loading"
        @keydown.enter.exact.prevent="send"
      />
      <p class="muted">Press Enter to send, Shift+Enter for a new line.</p>
      <p v-if="error" class="error">{{ error }}</p>
      <button type="button" :disabled="loading || !answer.trim()" @click="send">✉️ Send answer</button>
    </div>
  </template>

  <!-- ============ PHASE 3: feedback ============ -->
  <template v-else>
    <div v-if="loading" class="card">
      <p>Analyzing your interview...</p>
    </div>

    <div v-else-if="error" class="card">
      <p class="error">{{ error }}</p>
      <button type="button" @click="finish">🔄 Try again</button>
    </div>

    <InterviewFeedback v-else-if="feedback" :feedback="feedback" />

    <div class="toolbar">
      <button type="button" class="secondary" :disabled="loading" @click="restart">
        🔁 Start a new interview
      </button>
    </div>
  </template>
</template>
