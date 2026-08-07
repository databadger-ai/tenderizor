import { Bell, Building2, ChevronDown, CircleHelp, Landmark, LayoutDashboard, Search, ShieldCheck } from 'lucide-react'
import { OpportunityInbox } from './components/OpportunityInbox'
import { TenderWorkspace } from './components/TenderWorkspace'

export default function App() {
  const tenderMatch = /^\/tenders\/([^/]+)\/?$/.exec(window.location.pathname)
  const tenderId = tenderMatch ? decodeURIComponent(tenderMatch[1]) : null

  return (
    <div className="app-shell">
      <a href="#main-content" className="skip-link">Skip to main content</a>
      <header className="topbar">
        <a className="brand" href="/" aria-label="CanadaBuys Tender Workbench home"><span className="brand-mark"><Landmark aria-hidden="true" /></span><span><strong>CanadaBuys</strong><small>AI Tender Workbench</small></span></a>
        <nav className="primary-nav" aria-label="Primary navigation"><a className="active" href="/"><LayoutDashboard />Work inbox</a><button type="button" disabled><Building2 />Company readiness</button></nav>
        <div className="topbar-actions"><button type="button" className="icon-button" aria-label="Search"><Search /></button><button type="button" className="icon-button" aria-label="Help"><CircleHelp /></button><button type="button" className="icon-button notification-button" aria-label="Notifications"><Bell /><span className="notification-dot" /></button><button type="button" className="profile-button"><span>P0</span><span><strong>Phase 0 user</strong><small>Trading analyst</small></span><ChevronDown /></button></div>
      </header>
      <div className="safety-banner" role="note"><ShieldCheck aria-hidden="true" /><strong>Supervised mode</strong><span>AI can read, analyse, and draft. Only authorized humans decide or act externally.</span><span className="safety-badge">No autonomous submission</span></div>
      {tenderId ? <TenderWorkspace tenderId={tenderId} /> : <OpportunityInbox />}
    </div>
  )
}
