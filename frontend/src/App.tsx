import { useCallback, useEffect, useState } from 'react'
import { fetchOptions, predictFlight } from './api/client'
import { FlightForm } from './components/FlightForm'
import { PredictionPanel } from './components/PredictionPanel'
import { RouteMap } from './components/RouteMap'
import type { OptionsResponse, PredictionRequest, PredictionResponse } from './types'

function App() {
  const [options, setOptions] = useState<OptionsResponse | null>(null)
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null)
  const [loadError, setLoadError] = useState('')
  const [requestError, setRequestError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    const controller = new AbortController()
    fetchOptions(controller.signal)
      .then(setOptions)
      .catch((error: unknown) => {
        if (error instanceof DOMException && error.name === 'AbortError') return
        setLoadError(error instanceof Error ? error.message : 'Unable to load flight options.')
      })
    return () => controller.abort()
  }, [])

  const submitPrediction = useCallback(async (request: PredictionRequest) => {
    setIsSubmitting(true)
    setRequestError('')
    try {
      setPrediction(await predictFlight(request))
    } catch (error) {
      setRequestError(error instanceof Error ? error.message : 'Unable to get a prediction.')
    } finally {
      setIsSubmitting(false)
    }
  }, [])

  if (loadError) return <main className="loading-state"><h1>Flight Delay Forecast</h1><p>{loadError}</p></main>
  if (!options) return <main className="loading-state"><h1>Flight Delay Forecast</h1><p>Loading flight options…</p></main>

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <p className="product-name">Flight Delay Forecast</p>
          <h1>Plan with a clearer view of delay risk.</h1>
        </div>
        <p className="header-note">Model-backed estimates for supported U.S. airport routes.</p>
      </header>

      <section className="workspace" aria-label="Flight delay prediction">
        <div className="left-rail">
          <section className="form-card">
            <FlightForm airlines={options.airlines} airports={options.supported_airports} isSubmitting={isSubmitting} onSubmit={submitPrediction} />
          </section>
          {requestError && <p className="request-error" role="alert">{requestError}</p>}
          <PredictionPanel prediction={prediction} />
          <aside className="model-note"><h2>Model notes</h2><p>Weather inputs are historic monthly medians. Results are estimates, not guarantees.</p></aside>
        </div>
        <RouteMap prediction={prediction} />
      </section>
    </main>
  )
}

export default App
