import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { api } from './api'
import type { AnalysisRun, TenderDetail } from './types'

vi.mock('./api', () => ({
  api: {
    listTenders: vi.fn(),
    createTender: vi.fn(),
    getTender: vi.fn(),
    startAnalysis: vi.fn(),
    getAnalysisRun: vi.fn(),
    listActivity: vi.fn(),
    submitCorrection: vi.fn(),
  },
}))

const tender: TenderDetail = {
  id: 'tender-1',
  title: 'Secure network appliances',
  reference_number: 'REF-2026-44',
  solicitation_number: 'PW-26-1001',
  buyer: 'Shared Services Canada',
  deadline: '2026-09-10T18:00:00Z',
  line_count: 4,
  source_sha256: 'a'.repeat(64),
  latest_run_id: 'run-1',
  latest_run_status: 'SUCCEEDED',
  recommendation: 'REVIEW',
  gate_outcome: 'BID_BLOCKED',
  source_text: 'Mandatory security clearance.\nDelivery in Ottawa.\nRated experience: 5 years.\nClosing date applies.\n',
  created_at: '2026-08-01T12:00:00Z',
  updated_at: '2026-08-02T12:00:00Z',
}

const successfulRun: AnalysisRun = {
  run_id: 'run-1',
  tender_id: tender.id,
  workflow_id: 'workflow-1',
  status: 'SUCCEEDED',
  analysis: {
    model: 'openai:gpt-5.6-sol',
    definition_version: 'canadabuys_tender_analysis_v1',
    summary: 'Strong technical fit, but security clearance is not yet evidenced.',
    recommendation: 'REVIEW',
    confidence: 0.82,
    cited_material_fields: [{ field_name: 'delivery_location', value: 'Ottawa', citations: [{ line_start: 2, line_end: 2, quote: 'Delivery in Ottawa.' }] }],
    requirements: [{ requirement: 'Valid security clearance', requirement_type: 'MANDATORY', status: 'UNKNOWN', fatal: true, rationale: 'Company evidence was not supplied.', citations: [{ line_start: 1, line_end: 1, quote: 'Mandatory security clearance.' }] }],
    missing_facts: [{ fact: 'Security clearance', impact: 'Fatal eligibility gate remains unresolved.' }],
    risks: [],
    gate_outcome: 'BID_BLOCKED',
    gate_block_reasons: ['Mandatory security clearance is unresolved.'],
  },
  created_at: '2026-08-02T12:00:00Z',
  updated_at: '2026-08-02T12:01:00Z',
  completed_at: '2026-08-02T12:01:00Z',
}

describe('CanadaBuys workbench', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
    sessionStorage.clear()
    vi.mocked(api.listTenders).mockResolvedValue({ items: [tender], total: 1 })
    vi.mocked(api.getTender).mockResolvedValue(tender)
    vi.mocked(api.listActivity).mockResolvedValue({ items: [], total: 0 })
    vi.mocked(api.startAnalysis).mockResolvedValue({ run_id: 'run-1', workflow_id: 'workflow-1', status: 'QUEUED' })
    vi.mocked(api.getAnalysisRun).mockResolvedValue(successfulRun)
  })

  it('loads the opportunity inbox with safe operating boundaries', async () => {
    render(<App />)
    expect(screen.getByText('No autonomous submission')).toBeInTheDocument()
    expect(await screen.findByText('Secure network appliances')).toBeInTheDocument()
    expect(screen.getByText('Shared Services Canada')).toBeInTheDocument()
  })

  it('shows evidence, hard gate, requirements, and review controls after analysis', async () => {
    window.history.replaceState({}, '', '/tenders/tender-1')
    const user = userEvent.setup()
    render(<App />)

    expect(await screen.findByRole('heading', { name: 'Bid blocked' })).toBeInTheDocument()
    expect(screen.getByText('82%')).toBeInTheDocument()
    expect(screen.getByText(/canadabuys_tender_analysis_v1/)).toBeInTheDocument()

    await user.click(screen.getByRole('tab', { name: 'Evidence' }))
    expect(screen.getByLabelText('Line-addressable tender source').children).toHaveLength(4)

    await user.click(screen.getByRole('tab', { name: /Requirements/ }))
    expect(screen.getByText('Valid security clearance')).toBeInTheDocument()
    expect(screen.getByText('Fatal if unresolved')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Review' }))
    expect(screen.getByRole('dialog', { name: 'Review or correct finding' })).toBeInTheDocument()
    await waitFor(() => expect(screen.getByLabelText('Reason')).toHaveFocus())
  })
})
