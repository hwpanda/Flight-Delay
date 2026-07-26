import { useEffect } from 'react'
import { CircleMarker, MapContainer, Polyline, Popup, TileLayer, useMap } from 'react-leaflet'
import type { PredictionResponse } from '../types'

interface RouteMapProps {
  prediction: PredictionResponse | null
}

function RouteViewport({ prediction }: RouteMapProps) {
  const map = useMap()

  useEffect(() => {
    if (prediction) map.fitBounds([prediction.route.origin_coords, prediction.route.dest_coords], { padding: [44, 44] })
  }, [map, prediction])

  return null
}

export function RouteMap({ prediction }: RouteMapProps) {
  const route = prediction ? [prediction.route.origin_coords, prediction.route.dest_coords] : null

  return (
    <div className="map-shell" aria-label="Flight route map">
      <MapContainer center={[39.8283, -98.5795]} zoom={4} scrollWheelZoom className="route-map">
        <TileLayer attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <RouteViewport prediction={prediction} />
        {route && <Polyline positions={route} pathOptions={{ color: '#0f6cbd', weight: 4, opacity: 0.85 }} />}
        {prediction && <>
          <CircleMarker center={prediction.route.origin_coords} radius={8} pathOptions={{ color: '#0f6cbd', fillColor: '#0f6cbd', fillOpacity: 1 }}><Popup>Origin</Popup></CircleMarker>
          <CircleMarker center={prediction.route.dest_coords} radius={8} pathOptions={{ color: '#f97316', fillColor: '#f97316', fillOpacity: 1 }}><Popup>Destination</Popup></CircleMarker>
        </>}
      </MapContainer>
    </div>
  )
}
