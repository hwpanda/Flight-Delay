import { useMemo, useState, type FormEvent } from 'react'
import type { AirportOption, PredictionRequest } from '../types'

interface FlightFormProps {
  airlines: Record<string, string>
  airports: AirportOption[]
  isSubmitting: boolean
  onSubmit: (request: PredictionRequest) => Promise<void>
}

const initialForm: PredictionRequest = {
  flight_date: '',
  dep_time: '',
  arr_time: '',
  airline: '',
  origin: '',
  destination: '',
}

export function FlightForm({ airlines, airports, isSubmitting, onSubmit }: FlightFormProps) {
  const [form, setForm] = useState<PredictionRequest>(initialForm)
  const [validationMessage, setValidationMessage] = useState('')
  const supportedCodes = useMemo(() => new Set(airports.map((airport) => airport.code)), [airports])
  const airlineOptions = useMemo(
    () => Object.entries(airlines).sort(([, left], [, right]) => left.localeCompare(right)),
    [airlines],
  )

  const updateField = (field: keyof PredictionRequest, value: string) => {
    const normalized = field === 'origin' || field === 'destination' ? value.toUpperCase() : value
    setForm((current) => ({ ...current, [field]: normalized }))
    if (field === 'origin' || field === 'destination') setValidationMessage('')
  }

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const origin = form.origin.trim()
    const destination = form.destination.trim()
    if (!supportedCodes.has(origin) || !supportedCodes.has(destination)) {
      setValidationMessage('Choose origin and destination from the supported-airports list.')
      return
    }

    setValidationMessage('')
    await onSubmit({ ...form, origin, destination })
  }

  return (
    <form className="flight-form" onSubmit={submit}>
      <label className="field">
        <span>Flight date</span>
        <input type="date" value={form.flight_date} onChange={(event) => updateField('flight_date', event.target.value)} required />
      </label>

      <div className="time-grid">
        <label className="field">
          <span>Scheduled departure</span>
          <input type="time" value={form.dep_time} onChange={(event) => updateField('dep_time', event.target.value)} required />
        </label>
        <label className="field">
          <span>Scheduled arrival</span>
          <input type="time" value={form.arr_time} onChange={(event) => updateField('arr_time', event.target.value)} required />
        </label>
      </div>

      <label className="field">
        <span>Airline</span>
        <select value={form.airline} onChange={(event) => updateField('airline', event.target.value)} required>
          <option value="" disabled>Select airline</option>
          {airlineOptions.map(([code, name]) => <option key={code} value={code}>{name} ({code})</option>)}
        </select>
      </label>

      <section className="route-fields" aria-labelledby="route-heading">
        <div className="section-heading">
          <h2 id="route-heading">Route</h2>
          <p>Choose from {airports.length} airports currently supported by the weather data.</p>
        </div>
        <div className="time-grid">
          <label className="field">
            <span>Origin</span>
            <input type="text" list="supported-airports" value={form.origin} onChange={(event) => updateField('origin', event.target.value)} placeholder="ATL" maxLength={4} autoComplete="off" required />
          </label>
          <label className="field">
            <span>Destination</span>
            <input type="text" list="supported-airports" value={form.destination} onChange={(event) => updateField('destination', event.target.value)} placeholder="BOS" maxLength={4} autoComplete="off" required />
          </label>
        </div>
        <datalist id="supported-airports">
          {airports.map((airport) => <option key={airport.code} value={airport.code}>{airport.city}, {airport.state}</option>)}
        </datalist>
      </section>

      {validationMessage && <p className="form-error" role="alert">{validationMessage}</p>}
      <button className="primary-button" type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Calculating forecast…' : 'Predict delay'}
      </button>
    </form>
  )
}
