import { useState, useMemo, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents, Polyline, useMap } from 'react-leaflet'; 
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
  onRefresh?: () => Promise<void>;
}

function MapEvents({ onMapClick }: { onMapClick: () => void }) {
  useMapEvents({
    click: () => {
      onMapClick();
    },
  });
  return null;
}

function RouteFitter({ coords }: { coords: [number, number][] }) {
  const map = useMap();
  useEffect(() => {
    if (coords.length > 0) {
      map.fitBounds(coords, { padding: [50, 50], animate: true });
    }
  }, [coords, map]);
  return null;
}

const BRASOV_BOUNDS: L.LatLngBoundsExpression = [
  [45.50, 25.35], // Sud-Vest (dincolo de Cristian / Râșnov)
  [45.75, 25.80]  // Nord-Est (dincolo de Aeroport / Sânpetru / Săcele)
];

export default function MapView({ locations = mockLocations, onRefresh }: Props) {
  const [selected, setSelected] = useState<Location | null>(null);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [routeCoords, setRouteCoords] = useState<[number, number][]>([]);

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
      const timer = setTimeout(() => setSelected(filtered[0]), 10);
      return () => clearTimeout(timer);
    }
  }, [filtered]);

  const handleAISelectLocation = (id: number) => {
    const loc = locations.find(l => l.id === id);
    if (loc) {
      setSelected(loc);
    }
  };

  const handleAISelectRoute = async (startId: number, endId: number) => {
    const startLoc = locations.find(l => l.id === startId);
    const endLoc = locations.find(l => l.id === endId);
    
    if (startLoc && endLoc) {
      setSelected(endLoc);
      
      try {
        const response = await fetch(
          `https://router.project-osrm.org/route/v1/foot/${startLoc.lng},${startLoc.lat};${endLoc.lng},${endLoc.lat}?overview=full&geometries=geojson`
        );
        const data = await response.json();
        
        if (data.routes && data.routes.length > 0) {
          const coords = data.routes[0].geometry.coordinates.map(
            (coord: [number, number]) => [coord[1], coord[0]] as [number, number]
          );
          setRouteCoords(coords);
        }
      } catch (e) {
        console.error("Failed to fetch route", e);
      }
    }
  };

  return (
    <div style={{ position: 'relative', width: '100vw', height: '100vh', overflow: 'hidden' }}>
      <SearchBar value={search} onChange={setSearch} />
      {!selected && <FilterBar selected={category} onChange={setCategory} />}
      {!selected && (
  localStorage.getItem('token')
    ? <a href="/profile" style={{
        position: 'fixed', top: '1rem', right: '1rem',
        zIndex: 9999, background: '#2563eb', color: 'white',
        padding: '0.5rem 1rem', borderRadius: '8px',
        textDecoration: 'none', fontSize: '14px',
        boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
      }}>👤 Profil</a>
    : <a href="http://localhost:8000/auth/login" style={{
        position: 'fixed', top: '1rem', right: '1rem',
        zIndex: 9999, background: '#2563eb', color: 'white',
        padding: '0.5rem 1rem', borderRadius: '8px',
        textDecoration: 'none', fontSize: '14px',
        boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
      }}>🔐 Login</a>
)}

      {routeCoords.length > 0 && (
        <button
          onClick={() => setRouteCoords([])}
          style={{
            position: 'absolute',
            top: '80px',
            left: '10px',
            zIndex: 9999,
            background: 'white',
            color: '#dc2626',
            border: '2px solid rgba(0,0,0,0.2)',
            padding: '8px 12px',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: 'bold',
            boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
          }}
        >
          ✖ Șterge Traseul
        </button>
      )}

      <MapContainer
        center={[45.6427, 25.5887]}
        zoom={14}
        minZoom={11}
        maxBounds={BRASOV_BOUNDS}
        maxBoundsViscosity={1.0}
        style={{ width: '100%', height: '100vh', zIndex: 1 }}
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapController selected={selected} />

        <MapEvents onMapClick={() => { setSelected(null); }} />

        {filtered.map((loc) => (
          <Marker
            key={loc.id}
            position={[loc.lat, loc.lng]}
            eventHandlers={{ 
              click: () => {
                setSelected(loc);
              } 
            }}
          />
        ))}

        {routeCoords.length > 0 && (
          <>
            <Polyline 
              positions={routeCoords} 
              color="#3b82f6" 
              weight={6} 
              dashArray="10, 10" 
              opacity={0.8}
            />
            <RouteFitter coords={routeCoords} />
          </>
        )}
      </MapContainer>

      {selected && (
        <LocationPanel
          location={selected}
          onClose={() => setSelected(null)}
        />
      )}

      <AIAssistant 
        onSelectLocation={handleAISelectLocation} 
        onSelectRoute={handleAISelectRoute}
        onRefresh={onRefresh}
      />
    </div>
  );
}