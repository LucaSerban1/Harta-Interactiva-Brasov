import { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MapView from './components/MapView';
import AdminPage from './pages/AdminPage';
import AuthCallback from './pages/AuthCallback';
import { fetchLocations } from './api';
import type { Location } from './mockData';
import ProfilePage from './pages/ProfilePage';

function MapWrapper() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadLocations = async () => {
    try {
      const data = await fetchLocations();
      setLocations(data);
    } catch {
      setError('Nu s-a putut conecta la server');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLocations();
  }, []);

  const handleRefresh = async () => {
    await loadLocations();
  };

  if (loading) return <p style={{ padding: '2rem' }}>Se încarcă harta...</p>;
  if (error) return <p style={{ padding: '2rem', color: 'red' }}>{error}</p>;

  return <MapView locations={locations} onRefresh={handleRefresh} />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MapWrapper />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;