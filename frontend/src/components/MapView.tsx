import { useState } from 'react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { mockLocations } from '../mockData';
import type { Location } from '../mockData';
import LocationPanel from './LocationPanel';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

interface Props {
  locations?: Location[];
}

export default function MapView({ locations = mockLocations }: Props) {
  const [selected, setSelected] = useState<Location | null>(null);

  return (
    <div style={{ position: 'relative' }}>
      <MapContainer
        center={[45.6427, 25.5887]}
        zoom={14}
        style={{ width: '100%', height: '100vh' }}
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {locations.map((loc) => (
          <Marker
            key={loc.id}
            position={[loc.lat, loc.lng]}
            eventHandlers={{ click: () => setSelected(loc) }}
          />
        ))}
      </MapContainer>

      {selected && (
        <LocationPanel
          location={selected}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  );
}