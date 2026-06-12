import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BASE_URL } from '../api';

interface User {
  id: number;
  email: string;
  username: string;
  is_admin: boolean;
}

interface Review {
  id: number;
  text: string;
  rating: number;
  location_id: number;
  location_name?: string;
  created_at: string;
}

interface Location {
  id: number;
  name: string;
  category: string;
  rating_avg: number;
}

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [favorites, setFavorites] = useState<Location[]>([]);
  const [activeTab, setActiveTab] = useState<'info' | 'reviews' | 'favorites'>('info');
  const [newReview, setNewReview] = useState({ location_id: '', text: '', rating: 5 });
  const [locations, setLocations] = useState<Location[]>([]);
  const [msg, setMsg] = useState('');
  const navigate = useNavigate();

  const fetchReviews = async (token: string) => {
    const res = await fetch(`${BASE_URL}/reviews/my`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) setReviews(await res.json());
  };

  const fetchFavorites = async (token: string) => {
    const res = await fetch(`${BASE_URL}/favorites/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) setFavorites(await res.json());
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/'); return; }

    fetch(`${BASE_URL}/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    }).then(r => r.json()).then(setUser);

    fetch(`${BASE_URL}/locations/`)
      .then(r => r.json()).then(setLocations);

    fetchReviews(token);
    fetchFavorites(token);
  }, []);

  const handleAddReview = async () => {
    const token = localStorage.getItem('token');
    if (!newReview.location_id || !newReview.text) {
      setMsg('Completează toate câmpurile!');
      return;
    }
    const res = await fetch(`${BASE_URL}/reviews/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        location_id: parseInt(newReview.location_id),
        text: newReview.text,
        rating: newReview.rating
      })
    });
    if (res.ok) {
      setMsg('Review adăugat!');
      setNewReview({ location_id: '', text: '', rating: 5 });
      fetchReviews(token!);
    } else {
      setMsg('Eroare la adăugare.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  const tabStyle = (tab: string) => ({
    padding: '0.5rem 1rem', cursor: 'pointer', border: 'none',
    borderBottom: activeTab === tab ? '2px solid #2563eb' : '2px solid transparent',
    background: 'none', color: activeTab === tab ? '#2563eb' : '#666',
    fontWeight: activeTab === tab ? 600 : 400, fontSize: '14px'
  });

  const inputStyle = {
    width: '100%', padding: '0.5rem 0.75rem', borderRadius: '8px',
    border: '1px solid #e5e7eb', fontSize: '14px', color: 'black',
    background: 'white', marginBottom: '0.75rem', boxSizing: 'border-box' as const
  };

  if (!user) return <p style={{ padding: '2rem' }}>Se încarcă...</p>;

  return (
    <div style={{
      minHeight: '100vh', background: '#f3f4f6',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: '2rem'
    }}>
      <div style={{
        background: 'white', borderRadius: '16px', width: '100%',
        maxWidth: '480px', boxShadow: '0 4px 20px rgba(0,0,0,0.1)', color: 'black'
      }}>
        {/* Header profil */}
        <div style={{ padding: '2rem', textAlign: 'center', borderBottom: '1px solid #e5e7eb' }}>
          <div style={{
            width: '72px', height: '72px', borderRadius: '50%',
            background: '#2563eb', color: 'white', fontSize: '2rem',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 1rem'
          }}>
            {user.username[0].toUpperCase()}
          </div>
          <h2 style={{ margin: 0, color: 'black' }}>{user.username}</h2>
          <p style={{ color: '#555', marginTop: '0.25rem', fontSize: '14px' }}>{user.email}</p>
          {user.is_admin && (
            <span style={{
              background: '#fef3c7', color: '#92400e', fontSize: '12px',
              padding: '2px 10px', borderRadius: '20px', marginTop: '0.5rem',
              display: 'inline-block'
            }}>👑 Admin</span>
          )}
        </div>

        {/* Tab-uri */}
        <div style={{ display: 'flex', borderBottom: '1px solid #e5e7eb' }}>
          <button style={tabStyle('info')} onClick={() => setActiveTab('info')}>👤 Cont</button>
          <button style={tabStyle('reviews')} onClick={() => setActiveTab('reviews')}>⭐ Review-uri</button>
          <button style={tabStyle('favorites')} onClick={() => setActiveTab('favorites')}>❤️ Favorite</button>
        </div>

        {/* Continut tab-uri */}
        <div style={{ padding: '1.5rem' }}>

          {activeTab === 'info' && (
            <div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ fontSize: '12px', color: '#888' }}>USERNAME</label>
                <p style={{ margin: '4px 0', fontWeight: 500 }}>{user.username}</p>
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ fontSize: '12px', color: '#888' }}>EMAIL</label>
                <p style={{ margin: '4px 0', fontWeight: 500 }}>{user.email}</p>
              </div>
              <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ fontSize: '12px', color: '#888' }}>ROL</label>
                <p style={{ margin: '4px 0', fontWeight: 500 }}>{user.is_admin ? 'Administrator' : 'Utilizator'}</p>
              </div>
              <a href="/" style={{
                display: 'block', textAlign: 'center', marginBottom: '0.75rem',
                color: '#2563eb', textDecoration: 'none', fontSize: '14px'
              }}>← Înapoi la hartă</a>
              {user.is_admin && (
                <a href="/admin" style={{
                  display: 'block', textAlign: 'center', marginBottom: '0.75rem',
                  color: '#2563eb', textDecoration: 'none', fontSize: '14px'
                }}>🛠️ Admin Panel</a>
              )}
              <button onClick={handleLogout} style={{
                width: '100%', background: '#dc2626', color: 'white',
                border: 'none', padding: '0.6rem', borderRadius: '8px',
                cursor: 'pointer', fontSize: '14px'
              }}>Deconectare</button>
            </div>
          )}

          {activeTab === 'reviews' && (
            <div>
              <h3 style={{ marginTop: 0 }}>Adaugă review</h3>
              <select
                style={inputStyle}
                value={newReview.location_id}
                onChange={e => setNewReview(r => ({ ...r, location_id: e.target.value }))}
              >
                <option value="">Selectează locația...</option>
                {locations.map(loc => (
                  <option key={loc.id} value={loc.id}>{loc.name}</option>
                ))}
              </select>
              <textarea
                style={{ ...inputStyle, height: '80px', resize: 'none' }}
                placeholder="Scrie review-ul tău..."
                value={newReview.text}
                onChange={e => setNewReview(r => ({ ...r, text: e.target.value }))}
              />
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                <label style={{ fontSize: '14px', color: '#555' }}>Rating:</label>
                {[1,2,3,4,5].map(n => (
                  <button key={n} onClick={() => setNewReview(r => ({ ...r, rating: n }))}
                    style={{
                      background: 'none', border: 'none', cursor: 'pointer',
                      fontSize: '1.5rem', opacity: n <= newReview.rating ? 1 : 0.3
                    }}>⭐</button>
                ))}
              </div>
              <button onClick={handleAddReview} style={{
                width: '100%', background: '#2563eb', color: 'white',
                border: 'none', padding: '0.6rem', borderRadius: '8px',
                cursor: 'pointer', fontSize: '14px'
              }}>Trimite review</button>
              {msg && <p style={{ marginTop: '0.5rem', color: msg.includes('Eroare') ? 'red' : 'green', fontSize: '13px' }}>{msg}</p>}

              <h3 style={{ marginTop: '1.5rem', marginBottom: '0.75rem' }}>Istoricul meu</h3>
              {reviews.length === 0 ? (
                <p style={{ color: '#888', textAlign: 'center', fontSize: '14px' }}>Nu ai recenzii încă.</p>
              ) : (
                reviews.map(r => (
                  <div key={r.id} style={{
                    padding: '0.75rem', borderRadius: '8px', background: '#f9f9f9',
                    marginBottom: '0.5rem', borderLeft: '3px solid #2563eb'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                      <span style={{ fontWeight: 600, fontSize: '14px' }}>{r.location_name ?? `Locație #${r.location_id}`}</span>
                      <span style={{ fontSize: '13px' }}>{'⭐'.repeat(r.rating)}</span>
                    </div>
                    <p style={{ margin: 0, fontSize: '13px', color: '#444' }}>{r.text}</p>
                    <span style={{ fontSize: '11px', color: '#aaa' }}>
                      {new Date(r.created_at).toLocaleDateString('ro-RO')}
                    </span>
                  </div>
                ))
              )}
            </div>
          )}

          {activeTab === 'favorites' && (
            <div>
              {favorites.length === 0 ? (
                <p style={{ color: '#888', textAlign: 'center' }}>Nu ai locații favorite încă.</p>
              ) : (
                favorites.map(loc => (
                  <div key={loc.id} style={{
                    padding: '0.75rem', borderRadius: '8px', background: '#f9f9f9',
                    marginBottom: '0.5rem', display: 'flex', justifyContent: 'space-between'
                  }}>
                    <span style={{ fontWeight: 500 }}>{loc.name}</span>
                    <span style={{ color: '#888', fontSize: '13px' }}>⭐ {loc.rating_avg}</span>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}