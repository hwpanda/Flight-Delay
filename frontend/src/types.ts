export type Coordinates = [number, number]

export interface AirportOption {
  code: string
  city: string
  state: string
}

export interface OptionsResponse {
  airlines: Record<string, string>
  supported_airports: AirportOption[]
}

export interface PredictionRequest {
  flight_date: string
  dep_time: string
  arr_time: string
  airline: string
  origin: string
  destination: string
}

export interface PredictionResponse {
  delayed: boolean
  probability: number
  message: string
  features: Record<string, number>
  route: {
    origin_coords: Coordinates
    dest_coords: Coordinates
  }
}
