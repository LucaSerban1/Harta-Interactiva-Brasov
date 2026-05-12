import { useState, useMemo, useEffect } from 'react';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { mockLocations } from '../mockData';
import type { Location } from '../mockData';
import LocationPanel from './LocationPanel';
import SearchBar from './SearchBar';
import FilterBar from './FilterBar';
import MapController from './MapController';
import AIAssistant from './AIAssistant';

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
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');

  const filtered = useMemo(() => {
    const q = search.toLowerCase().trim();
    return locations.filter(loc => {
      const matchSearch = !q ||
        loc.name.toLowerCase().includes(q) ||
        loc.category.toLowerCase().includes(q) ||
        (loc.address ?? '').toLowerCase().includes(q) ||
        (loc.description ?? '').toLowerCase().includes(q) ||
        (loc.tags ?? []).some(tag => tag.toLowerCase().includes(q));
      const matchCategory = !category || loc.category === category;
      return matchSearch && matchCategory;
    });
  }, [search, category, locations]);

  useEffect(() => {
    if (filtered.length === 1) {
      setSelected(filtered[0]);
    }
  }, [filtered]);

  return (
    <div style={{ position: 'relative', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <SearchBar value={search} onChange={setSearch} />
      <FilterBar selected={category} onChange={setCategory} />
      <a
       href="http://localhost:8000/auth/login"
        style={{
          position: 'fixed', top: '1rem', right: '1rem',
          zIndex: 9999, background: '#2563eb', color: 'white',
          padding: '0.5rem 1rem', borderRadius: '8px',
          textDecoration: 'none', fontSize: '14px',
          boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
        }}
      >
        🔐 Login
      </a>
      <MapContainer
        center={[45.6427, 25.5887]}
        zoom={14}
        style={{ width: '100%', height: '100vh' }}
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MapController selected={selected} />
        {filtered.map((loc) => (
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

      <AIAssistant />
    </div>
  );
}