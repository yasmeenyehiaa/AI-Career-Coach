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
