import { AlertTriangle, CheckCircle2, CircleDot, Clock3, XCircle } from 'lucide-react'
import type { ReactNode } from 'react'

type Tone = 'positive' | 'warning' | 'danger' | 'neutral' | 'info'

const icons: Record<Tone, ReactNode> = {
  positive: <CheckCircle2 aria-hidden="true" />,
  warning: <AlertTriangle aria-hidden="true" />,
  danger: <XCircle aria-hidden="true" />,
  neutral: <CircleDot aria-hidden="true" />,
  info: <Clock3 aria-hidden="true" />,
}

export function StatusPill({ children, tone = 'neutral' }: { children: ReactNode; tone?: Tone }) {
  return (
    <span className={`status-pill status-pill--${tone}`}>
      {icons[tone]}
      {children}
    </span>
  )
}
