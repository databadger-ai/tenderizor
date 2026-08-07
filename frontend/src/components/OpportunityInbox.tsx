import { AlertCircle, ArrowRight, CalendarClock, FileSearch, Filter, Plus, Search, Sparkles } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { api } from '../api'
import type { CreateTenderInput, TenderSummary } from '../types'
import { CreateTenderDialog } from './CreateTenderDialog'
import { StatusPill } from './StatusPill'

function formatDate(value?: string | null) {
  if (!value) return 'Pending extraction'
  return new Intl.DateTimeFormat('en-CA', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value))
}

export function OpportunityInbox() {
  const [items, setItems] = useState<TenderSummary[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [creating, setCreating] = useState(false)
  const [createError, setCreateError] = useState<string | null>(null)

  const load = () => {
    const controller = new AbortController()
    setLoading(true)
    setError(null)
    api.listTenders(controller.signal)
      .then((data) => { setItems(data.items); setTotal(data.total) })
      .catch((reason: unknown) => {
        if ((reason as Error).name !== 'AbortError') setError(reason instanceof Error ? reason.message : 'Unable to load opportunities')
      })
      .finally(() => setLoading(false))
    return controller
  }

  useEffect(() => {
    const controller = load()
    return () => controller.abort()
  }, [])

  const filtered = useMemo(() => {
    const query = search.trim().toLocaleLowerCase()
    return query ? items.filter((item) => [item.title, item.solicitation_number, item.reference_number, item.buyer].some((value) => value?.toLocaleLowerCase().includes(query))) : items
  }, [items, search])

  const createTender = async (input: CreateTenderInput) => {
    setCreating(true)
    setCreateError(null)
    try {
      const tender = await api.createTender(input)
      window.location.assign(`/tenders/${encodeURIComponent(tender.id)}`)
    } catch (reason) {
      setCreateError(reason instanceof Error ? reason.message : 'Unexpected error')
    } finally {
      setCreating(false)
    }
  }

  return (
    <main id="main-content" className="page-shell">
      <section className="page-heading">
        <div>
          <p className="eyebrow">Opportunity intelligence</p>
          <h1>Work inbox</h1>
          <p className="page-description">Triage new opportunities, focus human review, and keep every conclusion connected to evidence.</p>
        </div>
        <button className="button button--primary" onClick={() => setDialogOpen(true)}><Plus aria-hidden="true" />Create tender</button>
      </section>

      <section className="stat-grid" aria-label="Inbox summary">
        <article className="stat-card"><div><span>Open workspaces</span><strong>{loading ? '—' : total}</strong></div><FileSearch aria-hidden="true" /></article>
        <article className="stat-card"><div><span>Needs human review</span><strong>{loading ? '—' : items.filter((item) => item.recommendation === 'REVIEW').length}</strong></div><AlertCircle aria-hidden="true" /></article>
        <article className="stat-card"><div><span>Analysis active</span><strong>{loading ? '—' : items.filter((item) => ['QUEUED', 'RUNNING'].includes(item.latest_run_status || '')).length}</strong></div><Sparkles aria-hidden="true" /></article>
      </section>

      <section className="panel opportunity-panel" aria-labelledby="opportunity-heading">
        <header className="panel-header">
          <div><h2 id="opportunity-heading">Tender opportunities</h2><p>{total} workspace{total === 1 ? '' : 's'} in this view</p></div>
          <div className="toolbar">
            <label className="search-box"><Search aria-hidden="true" /><span className="sr-only">Search tenders</span><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search title, buyer, solicitation…" /></label>
            <button type="button" className="button button--secondary" disabled><Filter aria-hidden="true" />Filters</button>
          </div>
        </header>

        {loading ? <div className="state-view" aria-live="polite"><span className="spinner" /><strong>Loading opportunities</strong><p>Retrieving the latest tender workspaces.</p></div> : null}
        {!loading && error ? <div className="state-view state-view--error" role="alert"><AlertCircle /><strong>Opportunities could not be loaded</strong><p>{error}</p><button className="button button--secondary" onClick={() => load()}>Try again</button></div> : null}
        {!loading && !error && filtered.length === 0 ? <div className="state-view"><FileSearch /><strong>{search ? 'No opportunities match your search' : 'No tender workspaces yet'}</strong><p>{search ? 'Try a title, buyer, reference, or solicitation number.' : 'Create a workspace by pasting an official tender notice.'}</p>{!search ? <button className="button button--primary" onClick={() => setDialogOpen(true)}><Plus />Create tender</button> : null}</div> : null}

        {!loading && !error && filtered.length > 0 ? (
          <div className="opportunity-list">
            {filtered.map((item) => (
              <a className="opportunity-row" href={`/tenders/${encodeURIComponent(item.id)}`} key={item.id}>
                <div className="opportunity-main">
                  <div className="opportunity-title"><h3>{item.title}</h3>{item.gate_outcome === 'BID_BLOCKED' ? <StatusPill tone="danger">Hard gate blocked</StatusPill> : item.recommendation ? <StatusPill tone={item.recommendation === 'INCLUDE' ? 'positive' : item.recommendation === 'EXCLUDE' ? 'danger' : 'warning'}>{item.recommendation === 'INCLUDE' ? 'Include' : item.recommendation === 'EXCLUDE' ? 'Exclude' : 'Review'}</StatusPill> : <StatusPill>Not analysed</StatusPill>}</div>
                  <p>{item.buyer || 'Buyer pending extraction'}</p>
                  <div className="opportunity-meta"><span>{item.solicitation_number || item.reference_number || 'Identifier pending'}</span><span><CalendarClock aria-hidden="true" />{formatDate(item.deadline)}</span><span>Updated {formatDate(item.updated_at)}</span></div>
                </div>
                <ArrowRight aria-hidden="true" className="row-arrow" />
              </a>
            ))}
          </div>
        ) : null}
      </section>

      <CreateTenderDialog open={dialogOpen} submitting={creating} error={createError} onClose={() => { setDialogOpen(false); setCreateError(null) }} onSubmit={createTender} />
    </main>
  )
}
