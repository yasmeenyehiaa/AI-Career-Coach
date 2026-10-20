// Saves past reviews in the browser (localStorage), so a refresh does not lose them.
// Only the REVIEW RESULTS are saved, never the CV text itself.

const KEY = 'cv-reviewer-history'
const MAX_ENTRIES = 5 // keep only the last few reviews

// localStorage can throw (private mode, storage full, corrupted data),
// so every access is wrapped in try/catch.

export function loadHistory() {
  try {
    const raw = localStorage.getItem(KEY)
    const data = raw ? JSON.parse(raw) : []
    return Array.isArray(data) ? data : []
  } catch {
    return []
  }
}

export function saveHistory(history) {
  try {
    localStorage.setItem(KEY, JSON.stringify(history.slice(-MAX_ENTRIES)))
  } catch {
    // not critical: the app still works without saving
  }
}

export function clearHistory() {
  try {
    localStorage.removeItem(KEY)
  } catch {
    // ignore
  }
}
