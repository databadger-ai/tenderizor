import { expect, test } from '@playwright/test'

const tender = {
  id: '11111111-1111-4111-8111-111111111111',
  title: 'Supply of secure network appliances',
  reference_number: 'REF-2026-44',
  solicitation_number: 'PW-26-1001',
  buyer: 'Shared Services Canada',
  deadline: '2026-09-10T18:00:00Z',
  line_count: 4,
  source_sha256: 'a'.repeat(64),
  latest_run_id: '22222222-2222-4222-8222-222222222222',
  latest_run_status: 'SUCCEEDED',
  recommendation: 'REVIEW',
  gate_outcome: 'BID_BLOCKED',
  source_text: 'Mandatory security clearance.\nDelivery in Ottawa.\nRated experience: 5 years.\nClosing date applies.',
  created_at: '2026-08-01T12:00:00Z',
  updated_at: '2026-08-02T12:00:00Z',
}

test.beforeEach(async ({ page }) => {
  await page.route('**/api/v1/tenders', async (route) => {
    if (route.request().method() === 'POST') return route.fulfill({ json: tender })
    return route.fulfill({ json: { items: [tender], total: 1 } })
  })
  await page.route(`**/api/v1/tenders/${tender.id}`, (route) => route.fulfill({ json: tender }))
  await page.route(`**/api/v1/tenders/${tender.id}/activity`, (route) => route.fulfill({ json: { items: [], total: 0 } }))
  await page.route(`**/api/v1/tenders/${tender.id}/analysis-runs`, (route) => route.fulfill({ status: 202, json: { run_id: '22222222-2222-4222-8222-222222222222', workflow_id: 'tender-analysis-1', status: 'QUEUED' } }))
  await page.route('**/api/v1/analysis-runs/**', (route) => route.fulfill({ json: {
    run_id: '22222222-2222-4222-8222-222222222222', tender_id: tender.id, workflow_id: 'tender-analysis-1', status: 'SUCCEEDED',
    analysis: {
      model: 'openai:gpt-5.6-sol', definition_version: 'canadabuys_tender_analysis_v1',
      summary: 'Technical fit exists, but mandatory clearance is unresolved.', recommendation: 'REVIEW', confidence: 0.82,
      cited_material_fields: [{ field_name: 'delivery_location', value: 'Ottawa', citations: [{ line_start: 2, line_end: 2, quote: 'Delivery in Ottawa.' }] }],
      requirements: [{ requirement: 'Valid security clearance', requirement_type: 'MANDATORY', status: 'UNKNOWN', fatal: true, rationale: 'Evidence not supplied.', citations: [{ line_start: 1, line_end: 1, quote: 'Mandatory security clearance.' }], remediation: 'Compliance lead must verify current clearance.' }],
      missing_facts: [{ fact: 'Security clearance', impact: 'Blocks bid eligibility.' }], risks: [], gate_outcome: 'BID_BLOCKED', gate_block_reasons: ['Mandatory security clearance is unresolved.'],
    }, error_code: null, created_at: '2026-08-02T12:00:00Z', updated_at: '2026-08-02T12:01:00Z', completed_at: '2026-08-02T12:01:00Z',
  } }))
})

test('analyst can trace a blocked recommendation to source evidence', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: 'Work inbox' })).toBeVisible()
  await page.getByRole('link', { name: /Supply of secure network appliances/ }).click()
  await expect(page.locator('#main-content').getByText('No autonomous submission')).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Bid blocked' })).toBeVisible()
  await page.getByRole('tab', { name: /Evidence/ }).click()
  await expect(page.getByText('Delivery in Ottawa.').first()).toBeVisible()
  await page.getByRole('tab', { name: /Requirements/ }).click()
  await expect(page.getByText('Fatal if unresolved')).toBeVisible()
})
