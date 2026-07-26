import type { PredictionResponse } from '../types'

interface PredictionPanelProps {
  prediction: PredictionResponse | null
}

export function PredictionPanel({ prediction }: PredictionPanelProps) {
  if (!prediction) {
    return <aside className="result-card result-empty" aria-live="polite"><span className="result-label">Prediction</span><p>Enter a flight to see its delay forecast.</p></aside>
  }

  return (
    <aside className={`result-card ${prediction.delayed ? 'result-delayed' : 'result-on-time'}`} aria-live="polite">
      <span className="result-label">Prediction</span>
      <strong>{prediction.delayed ? 'Likely delayed' : 'Likely on time'}</strong>
      <p>{prediction.message}</p>
      <div className="probability-row"><span>Delay probability</span><b>{(prediction.probability * 100).toFixed(1)}%</b></div>
    </aside>
  )
}
