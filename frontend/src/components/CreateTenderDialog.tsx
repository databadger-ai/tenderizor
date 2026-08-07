import { FilePlus2, ShieldCheck, X } from 'lucide-react'
import { FormEvent, useEffect, useRef, useState } from 'react'
import type { CreateTenderInput } from '../types'

const initialForm: CreateTenderInput = {
  title: '',
  solicitation_number: '',
  buyer: '',
  deadline: '',
  source_text: '',
}

export function CreateTenderDialog({
  open,
  submitting,
  error,
  onClose,
  onSubmit,
}: {
  open: boolean
  submitting: boolean
  error: string | null
  onClose: () => void
  onSubmit: (input: CreateTenderInput) => Promise<void>
}) {
  const [form, setForm] = useState(initialForm)
  const titleRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (open) titleRef.current?.focus()
  }, [open])

  if (!open) return null

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    await onSubmit(form)
  }

  return (
    <div className="dialog-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="dialog-panel" role="dialog" aria-modal="true" aria-labelledby="create-title">
        <header className="dialog-header">
          <div className="dialog-heading">
            <span className="dialog-icon"><FilePlus2 aria-hidden="true" /></span>
            <div>
              <p className="eyebrow">Manual intake</p>
              <h2 id="create-title">Create tender workspace</h2>
            </div>
          </div>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Close create tender dialog"><X /></button>
        </header>

        <form onSubmit={submit} className="dialog-form">
          <div className="form-grid">
            <label className="field field--wide">
              <span>Tender title</span>
              <input ref={titleRef} required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} placeholder="e.g. Supply of network security appliances" />
            </label>
            <label className="field">
              <span>Solicitation number</span>
              <input required value={form.solicitation_number} onChange={(e) => setForm({ ...form, solicitation_number: e.target.value })} placeholder="PW-26-010245" />
            </label>
            <label className="field">
              <span>Buyer</span>
              <input required value={form.buyer} onChange={(e) => setForm({ ...form, buyer: e.target.value })} placeholder="Department or agency" />
            </label>
            <label className="field field--wide">
              <span>Closing deadline</span>
              <input required type="datetime-local" value={form.deadline} onChange={(e) => setForm({ ...form, deadline: e.target.value })} />
              <small>Enter the source time zone in the pasted notice until the official deadline is verified.</small>
            </label>
            <label className="field field--wide">
              <span>Source text</span>
              <textarea required rows={10} value={form.source_text} onChange={(e) => setForm({ ...form, source_text: e.target.value })} placeholder="Paste the official tender notice or document text…" />
              <small>Source content is treated as untrusted evidence, never as system instructions.</small>
            </label>
          </div>

          {error ? <div className="inline-alert inline-alert--danger" role="alert"><strong>Could not create tender.</strong> {error}</div> : null}

          <footer className="dialog-footer">
            <div className="safety-note"><ShieldCheck aria-hidden="true" /><span>Creates an internal, draft-only workspace. Nothing is sent to the buyer.</span></div>
            <div className="button-row">
              <button className="button button--secondary" type="button" onClick={onClose}>Cancel</button>
              <button className="button button--primary" type="submit" disabled={submitting}>{submitting ? 'Creating…' : 'Create workspace'}</button>
            </div>
          </footer>
        </form>
      </section>
    </div>
  )
}
