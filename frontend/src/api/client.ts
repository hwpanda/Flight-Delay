import type { OptionsResponse, PredictionRequest, PredictionResponse } from '../types'

async function readResponse<T>(response: Response): Promise<T> {
  const body = await response.json().catch(() => null)
  if (!response.ok) {
    const message = body && typeof body.error === 'string' ? body.error : 'Unable to complete the request.'
    throw new Error(message)
  }
  return body as T
}

export async function fetchOptions(signal?: AbortSignal): Promise<OptionsResponse> {
  return readResponse<OptionsResponse>(await fetch('/api/options', { signal }))
}

export async function predictFlight(payload: PredictionRequest): Promise<PredictionResponse> {
  return readResponse<PredictionResponse>(await fetch('/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }))
}
