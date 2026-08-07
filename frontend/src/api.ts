import type {
  AnalysisRun,
  AuditEvent,
  CorrectionInput,
  CreateTenderInput,
  TenderDetail,
  TenderSummary,
} from './types'

const apiBase = (import.meta.env.VITE_API_URL || '/api/v1').replace(/\/$/, '')

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly requestId?: string,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', Accept: 'application/json', ...options?.headers },
  })
  if (!response.ok) {
    const payload = (await response.json().catch(() => null)) as
      | { error?: { message?: string; request_id?: string } }
      | null
    throw new ApiError(payload?.error?.message || `Request failed (${response.status})`, response.status, payload?.error?.request_id)
  }
  return response.json() as Promise<T>
}

export const api = {
  async listTenders(signal?: AbortSignal) {
    return request<{ items: TenderSummary[]; total: number }>('/tenders', { signal })
  },
  async createTender(input: CreateTenderInput) {
    return request<TenderDetail>('/tenders', {
      method: 'POST',
      body: JSON.stringify({
        title: input.title,
        solicitation_number: input.solicitation_number,
        buyer: input.buyer,
        deadline: new Date(input.deadline).toISOString(),
        source_text: input.source_text,
      }),
    })
  },
  async getTender(id: string, signal?: AbortSignal) {
    return request<TenderDetail>(`/tenders/${encodeURIComponent(id)}`, { signal })
  },
  async startAnalysis(id: string) {
    return request<{ run_id: string; workflow_id: string; status: 'QUEUED' }>(
      `/tenders/${encodeURIComponent(id)}/analysis-runs`,
      { method: 'POST', body: JSON.stringify({ requested_by: 'current-user' }) },
    )
  },
  async getAnalysisRun(runId: string, signal?: AbortSignal) {
    return request<AnalysisRun>(`/analysis-runs/${encodeURIComponent(runId)}`, { signal })
  },
  async listActivity(id: string, signal?: AbortSignal) {
    return request<{ items: AuditEvent[]; total: number }>(`/tenders/${encodeURIComponent(id)}/activity`, { signal })
  },
  async submitCorrection(id: string, input: CorrectionInput) {
    return request<AuditEvent>(`/tenders/${encodeURIComponent(id)}/corrections`, {
      method: 'POST',
      body: JSON.stringify(input),
    })
  },
}
