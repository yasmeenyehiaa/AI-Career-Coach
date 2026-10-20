// Builds a PDF of the review in the browser and downloads it.
import { formatDelta, scoreBand } from './scores'

export async function downloadReviewPdf(review, role, previous = null) {
  // Load jsPDF only when the user clicks "Download" (keeps the first page load small)
  const { jsPDF } = await import('jspdf')

  const doc = new jsPDF({ unit: 'pt', format: 'a4' })
  const margin = 48
  const pageWidth = doc.internal.pageSize.getWidth()
  const pageHeight = doc.internal.pageSize.getHeight()
  const textWidth = pageWidth - margin * 2
  let y = margin // current vertical position on the page

  // Writes wrapped text and starts a new page when we run out of space
  function write(text, { size = 11, bold = false, indent = 0, gap = 4 } = {}) {
    doc.setFont('helvetica', bold ? 'bold' : 'normal')
    doc.setFontSize(size)
    doc.setTextColor(31, 41, 51)
    const lineHeight = size * 1.35
    const lines = doc.splitTextToSize(String(text), textWidth - indent)
    for (const line of lines) {
      if (y + lineHeight > pageHeight - margin) {
        doc.addPage()
        y = margin
      }
      doc.text(line, margin + indent, y + size)
      y += lineHeight
    }
    y += gap
  }

  function bullets(items) {
    items.forEach((item) => write(`- ${item}`, { indent: 12, gap: 2 }))
    y += 4
  }

  const capitalize = (text) => text.charAt(0).toUpperCase() + text.slice(1)

  // ---- content ----
  write('CV Review', { size: 20, bold: true, gap: 2 })
  write(`Target role: ${role}`, { gap: 2 })
  write(new Date().toLocaleDateString(), { gap: 14 })

  write(`Overall score: ${review.overall_score}/100 (${scoreBand(review.overall_score).label})`, {
    size: 14,
    bold: true,
  })
  if (previous) {
    const delta = review.overall_score - previous.overall_score
    write(`Change since your previous review: ${formatDelta(delta)} points`)
  }
  write(review.summary, { gap: 12 })

  write('Top priorities', { size: 14, bold: true })
  review.top_priorities.forEach((item, i) => write(`${i + 1}. ${item}`, { indent: 12, gap: 2 }))
  y += 10

  for (const section of review.sections) {
    write(`${capitalize(section.name)} - ${scoreBand(section.score).label} (${section.score}/100)`, {
      size: 13,
      bold: true,
    })
    write('Strengths', { bold: true, gap: 2 })
    bullets(section.strengths)
    write('Suggestions', { bold: true, gap: 2 })
    bullets(section.suggestions)
    y += 6
  }

  if (review.missing_skills.length) {
    write('Missing skills', { size: 14, bold: true })
    write(review.missing_skills.join(', '))
  }

  // File name from the role, e.g. "cv-review-junior-data-analyst.pdf"
  const slug = role.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'review'
  doc.save(`cv-review-${slug}.pdf`)
}
