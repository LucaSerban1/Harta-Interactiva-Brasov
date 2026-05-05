import { useEffect, useState } from 'react';
import MapView from './components/MapView';
import { fetchLocations } from './api';
import type { Location } from './mockData';

function App() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLocations()
      .then(data => setLocations(data))
      .catch(() => setError('Nu s-a putut conecta la server'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={{ padding: '2rem' }}>Se încarcă harta...</p>;
  if (error) return <p style={{ padding: '2rem', color: 'red' }}>{error}</p>;

  return <MapView locations={locations} />;
}

export default App;