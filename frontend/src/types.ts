export type RunStatus = 'QUEUED' | 'RUNNING' | 'SUCCEEDED' | 'FAILED'
export type Recommendation = 'INCLUDE' | 'REVIEW' | 'EXCLUDE'
export type RequirementType = 'MANDATORY' | 'RATED' | 'READINESS'
export type RequirementStatus = 'PASS' | 'REMEDIABLE' | 'FAIL' | 'UNKNOWN'

export interface Citation {
  line_start: number
  line_end: number
  quote: string
}

export interface TenderSummary {
  id: string
  title: string
  reference_number: string | null
  solicitation_number: string | null
  buyer?: string | null
  deadline?: string | null
  source_sha256: string
  line_count: number
  created_at: string
  updated_at: string
  latest_run_id: string | null
  latest_run_status: RunStatus | null
  recommendation: Recommendation | null
  gate_outcome: 'BID_ALLOWED' | 'BID_BLOCKED' | null
}

export interface TenderDetail extends TenderSummary {
  source_text: string
}

export interface CreateTenderInput {
  title: string
  solicitation_number: string
  buyer: string
  deadline: string
  source_text: string
}

export interface MaterialField {
  field_name: string
  value: unknown
  citations: Citation[]
}

export interface Requirement {
  requirement: string
  requirement_type: RequirementType
  status: RequirementStatus
  fatal: boolean
  rationale: string
  citations: Citation[]
  remediation?: string | null
}

export interface Analysis {
  model: string
  definition_version: string
  summary: string
  recommendation: Recommendation
  confidence: number
  cited_material_fields: MaterialField[]
  requirements: Requirement[]
  missing_facts: Array<{ fact: string; impact: string }>
  risks: Array<{ risk: string; severity: number; rationale: string; citations: Citation[] }>
  gate_outcome: 'BID_ALLOWED' | 'BID_BLOCKED'
  gate_block_reasons: string[]
}

export interface AnalysisRun {
  run_id: string
  tender_id: string
  workflow_id: string
  status: RunStatus
  analysis: Analysis | null
  error_code?: string | null
  created_at: string
  updated_at: string
  completed_at?: string | null
}

export interface AuditEvent {
  id: string
  tender_id: string
  analysis_run_id?: string | null
  action: string
  actor_id: string
  reason: string
  field_path: string
  previous_value?: unknown
  corrected_value?: unknown
  correlation_id: string
  occurred_at: string
}

export interface CorrectionInput {
  actor_id: string
  action: 'CORRECTION' | 'REVIEW'
  reason: string
  analysis_run_id?: string | null
  field_path: string
  previous_value?: unknown
  corrected_value?: unknown
}
