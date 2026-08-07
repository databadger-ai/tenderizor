import { CheckCircle2, X } from 'lucide-react'
import { FormEvent, useEffect, useRef, useState } from 'react'

export function CorrectionDialog({
  open,
  fieldPath,
  previousValue,
  submitting,
  error,
  onClose,
  onSubmit,
}: {
  open: boolean
  fieldPath: string
  previousValue: unknown
  submitting: boolean
  error: string | null
  onClose: () => void
  onSubmit: (input: { action: 'CORRECTION' | 'REVIEW'; reason: string; correctedValue?: string }) => Promise<void>
}) {
  const [action, setAction] = useState<'CORRECTION' | 'REVIEW'>('REVIEW')
  const [reason, setReason] = useState('')
  const [correctedValue, setCorrectedValue] = useState('')
  const reasonRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (open) reasonRef.current?.focus()
  }, [open])

  if (!open) return null
  const submit = async (event: FormEvent) => {
    event.preventDefault()
    await onSubmit({ action, reason, correctedValue: action === 'CORRECTION' ? correctedValue : undefined })
  }

  return (
    <div className="dialog-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="dialog-panel dialog-panel--small" role="dialog" aria-modal="true" aria-labelledby="review-title">
        <header className="dialog-header">
          <div className="dialog-heading"><span className="dialog-icon"><CheckCircle2 /></span><div><p className="eyebrow">Human control</p><h2 id="review-title">Review or correct finding</h2></div></div>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Close review dialog"><X /></button>
        </header>
        <form className="dialog-form" onSubmit={submit}>
          <div className="review-target"><span>Finding</span><strong>{fieldPath}</strong><small>Current value: {String(previousValue ?? 'Not provided')}</small></div>
          <fieldset className="segmented-control"><legend>Action</legend><label><input type="radio" name="action" checked={action === 'REVIEW'} onChange={() => setAction('REVIEW')} /><span>Confirm review</span></label><label><input type="radio" name="action" checked={action === 'CORRECTION'} onChange={() => setAction('CORRECTION')} /><span>Correct value</span></label></fieldset>
          {action === 'CORRECTION' ? <label className="field"><span>Corrected value</span><input required value={correctedValue} onChange={(e) => setCorrectedValue(e.target.value)} /></label> : null}
          <label className="field" htmlFor="review-reason"><span>Reason</span></label><textarea id="review-reason" className="review-reason" ref={reasonRef} required minLength={5} rows={4} value={reason} onChange={(e) => setReason(e.target.value)} placeholder="Explain the evidence and judgment behind this decision…" /><small className="field-help">Reasons become part of the append-only audit timeline.</small>
          {error ? <div className="inline-alert inline-alert--danger" role="alert">{error}</div> : null}
          <footer className="dialog-footer"><p className="muted">This records human judgment; it does not modify the original source.</p><div className="button-row"><button type="button" className="button button--secondary" onClick={onClose}>Cancel</button><button type="submit" className="button button--primary" disabled={submitting}>{submitting ? 'Recording…' : 'Record decision'}</button></div></footer>
        </form>
      </section>
    </div>
  )
}
