const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '') ?? ''

export async function reviewCv({ role, jobDescription, cvText, file }) {
  if (!apiBaseUrl && !import.meta.env.DEV) {
    throw new Error('Backend URL is not configured. Set VITE_API_BASE_URL in the frontend deployment.')
  }

  // A file can only be sent together with other fields as multipart form data
  const formData = new FormData()
  formData.append('role', role)
  if (jobDescription) formData.append('job_description', jobDescription)

  // The backend wants EITHER a file OR text, never both
  if (file) formData.append('file', file)
  else formData.append('cv_text', cvText)

  let response
  try {
    response = await fetch(`${apiBaseUrl}/api/cv/review`, { method: 'POST', body: formData })
  } catch {
    throw new Error('Could not reach the server. Is the backend running?')
  }

  if (!response.ok) {
    let message = 'Something went wrong. Please try again.'
    try {
      const body = await response.json()
      // Our own errors send a string in "detail"; validation errors send a list
      if (typeof body.detail === 'string') message = body.detail
    } catch {
      // response was not JSON, keep the default message
    }
    throw new Error(message)
  }

  return response.json()
}

// Shared helper: sends the request, turns errors into readable messages, returns the JSON.
async function request(url, options) {
  let response
  try {
    response = await fetch(url, options)
  } catch {
    throw new Error('Could not reach the server. Is the backend running?')
  }

  if (!response.ok) {
    let message = 'Something went wrong. Please try again.'
    try {
      const body = await response.json()
      if (typeof body.detail === 'string') {
        message = body.detail // our own errors send a string in "detail"
      } else if (Array.isArray(body.detail)) {
        message = 'Some input is invalid or too long. Please check it and try again.'
      }
    } catch {
      // response was not JSON, keep the default message
    }
    throw new Error(message)
  }

  return response.json()
}

// Sends JSON (used by the interview endpoints)
function postJson(url, body) {
  return request(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
}


export function startInterview(setup) {
  return postJson(`${apiBaseUrl}/api/interview/start`, setup)
}

export function sendAnswer(setup, messages) {
  return postJson(`${apiBaseUrl}/api/interview/answer`, { ...setup, messages })
}

export function getInterviewFeedback(setup, messages) {
  return postJson(`${apiBaseUrl}/api/interview/feedback`, { ...setup, messages })
}



// ---------------------------------------------------------------- Answer coach

// Asks the server for a random interview question (role and category are optional)
export function generateQuestion(role, category) {
  return postJson(`${apiBaseUrl}/api/coach/question`, {
    role,
    category,
  })
}

// The fixed list of themes the user can choose from
export function getCategories() {
  return request(`${apiBaseUrl}/api/coach/categories`)
}
// Analyzes a draft answer with STAR
export function analyzeAnswer({ question, answer, role }) {
  return postJson(`${apiBaseUrl}/api/coach/analyze`, { question, answer, role })
}