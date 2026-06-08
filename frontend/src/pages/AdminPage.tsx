import { useEffect, useState } from 'react';

interface Location {
  id: number;
  name: string;
  lat: number;
  lng: number;
  category: string;
  description?: string;
  tags?: string[];
  is_verified?: boolean;
  rating_avg?: number;
}

interface Stats {
  locations: number;
  reviews: number;
}

interface Report {
  id: number;
  review_id: number;
  reason: string;
  created_at: string;
  review_text?: string;
  reporter?: { id: number; username: string; is_admin: boolean };
}

const BASE = 'http://localhost:8000';

export default function AdminPage() {
  const [locations, setLocations] = useState<Location[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [stats, setStats] = useState<Stats>({ locations: 0, reviews: 0 });
  const [form, setForm] = useState({
    name: '', lat: '', lng: '', category: '', description: '', tags: ''
  });
  const [msg, setMsg] = useState('');

  const token = localStorage.getItem('token');
  const authHeaders = { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) };

  const loadReports = () => {
    fetch(`${BASE}/reviews/reports`, { headers: authHeaders })
      .then(r => r.ok ? r.json() : [])
      .then(setReports);
  };

  const loadLocations = () => {
    fetch(`${BASE}/locations/`)
      .then(r => r.json())
      .then(data => {
        setLocations(data);
        setStats(s => ({ ...s, locations: data.length }));
      });
  };

  useEffect(() => { loadLocations(); loadReports(); }, []);

  const handleDelete = async (id: number) => {
    if (!confirm('Sigur vrei să ștergi?')) return;
    await fetch(`${BASE}/locations/${id}`, { method: 'DELETE' });
    loadLocations();
  };

  const handleDismissReport = async (reportId: number) => {
    await fetch(`${BASE}/reviews/reports/${reportId}`, { method: 'DELETE', headers: authHeaders });
    loadReports();
  };

  const handleDeleteReview = async (reviewId: number, reportId: number) => {
    if (!confirm('Ștergi recenzia și raportul?')) return;
    await fetch(`${BASE}/reviews/${reviewId}`, { method: 'DELETE', headers: authHeaders });
    await fetch(`${BASE}/reviews/reports/${reportId}`, { method: 'DELETE', headers: authHeaders });
    loadReports();
  };

  const handleApprove = async (id: number) => {
    await fetch(`${BASE}/locations/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_verified: true })
    });
    loadLocations();
  };

  const handleSubmit = async () => {
    if (!form.name || !form.lat || !form.lng || !form.category) {
      setMsg('Completează câmpurile obligatorii!');
      return;
    }
    const res = await fetch(`${BASE}/locations/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: form.name,
        lat: parseFloat(form.lat),
        lng: parseFloat(form.lng),
        category: form.category,
        description: form.description,
        tags: form.tags.split(',').map(t => t.trim()).filter(Boolean),
        is_verified: false,
        rating_avg: 0
      })
    });
    if (res.ok) {
      setMsg('Locație adăugată!');
      setForm({ name: '', lat: '', lng: '', category: '', description: '', tags: '' });
      loadLocations();
    } else {
      setMsg('Eroare la adăugare.');
    }
  };

  const inputStyle = {
    padding: '0.4rem 0.6rem', borderRadius: '6px',
    border: '1px solid #ccc', fontSize: '14px', width: '100%',
    marginBottom: '0.5rem', boxSizing: 'border-box' as const
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '1100px', margin: '0 auto', color: 'black', background: 'white', minHeight: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ margin: 0, color: 'black' }}>🛠️ Admin Panel</h1>
        <a href="/" style={{ textDecoration: 'none', color: '#2563eb' }}>← Înapoi la hartă</a>
      </div>

      {/* Statistici */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        {[
          { label: 'Locații', value: stats.locations, color: '#dbeafe' },
          { label: 'Categorie unică', value: new Set(locations.map(l => l.category)).size, color: '#dcfce7' },
          { label: 'Verificate', value: locations.filter(l => l.is_verified).length, color: '#fef9c3' },
        ].map(s => (
          <div key={s.label} style={{
            background: s.color, borderRadius: '10px',
            padding: '1rem 1.5rem', flex: 1, textAlign: 'center'
          }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{s.value}</div>
            <div style={{ fontSize: '13px', color: 'black' }}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Formular adăugare */}
      <div style={{ background: '#f9f9f9', borderRadius: '10px', padding: '1.5rem', marginBottom: '2rem' }}>
        <h2 style={{ marginTop: 0 , color: 'black' }}>➕ Adaugă locație nouă</h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
          <input style={inputStyle} placeholder="Nume *" value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} />
          <input style={inputStyle} placeholder="Categorie * (cafe, park...)" value={form.category} onChange={e => setForm(f => ({ ...f, category: e.target.value }))} />
          <input style={inputStyle} placeholder="Latitudine * (ex: 45.6430)" value={form.lat} onChange={e => setForm(f => ({ ...f, lat: e.target.value }))} />
          <input style={inputStyle} placeholder="Longitudine * (ex: 25.5887)" value={form.lng} onChange={e => setForm(f => ({ ...f, lng: e.target.value }))} />
          <input style={{ ...inputStyle, gridColumn: 'span 2' }} placeholder="Descriere" value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))} />
          <input style={{ ...inputStyle, gridColumn: 'span 2' }} placeholder="Taguri (separate prin virgulă: wifi, linistit)" value={form.tags} onChange={e => setForm(f => ({ ...f, tags: e.target.value }))} />
        </div>
        <button onClick={handleSubmit} style={{
          background: '#2563eb', color: 'white', border: 'none',
          padding: '0.6rem 1.5rem', borderRadius: '6px', cursor: 'pointer', fontSize: '14px'
        }}>Adaugă locație</button>
        {msg && <span style={{ marginLeft: '1rem', color: msg.includes('Eroare') ? 'red' : 'green' }}>{msg}</span>}
      </div>

      {/* Rapoarte recenzii */}
      <h2 style={{ color: 'black', marginTop: '2rem' }}>🚩 Recenzii raportate ({reports.length})</h2>
      {reports.length === 0 ? (
        <p style={{ color: '#888' }}>Nu există rapoarte momentan.</p>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', marginBottom: '2rem' }}>
          <thead>
            <tr style={{ background: '#fef2f2' }}>
              {['Raportat de', 'Recenzie', 'Motiv', 'Data', 'Acțiuni'].map(h => (
                <th key={h} style={{ padding: '0.6rem', textAlign: 'left', borderBottom: '1px solid #fca5a5', color: 'black' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {reports.map(rep => (
              <tr key={rep.id} style={{ borderBottom: '1px solid #fee2e2' }}>
                <td style={{ padding: '0.6rem', color: 'black' }}>{rep.reporter?.username ?? '—'}</td>
                <td style={{ padding: '0.6rem', color: '#444', maxWidth: '200px' }}>{rep.review_text ?? `#${rep.review_id}`}</td>
                <td style={{ padding: '0.6rem', color: 'black' }}>{rep.reason}</td>
                <td style={{ padding: '0.6rem', color: '#888', whiteSpace: 'nowrap' }}>{new Date(rep.created_at).toLocaleDateString('ro-RO')}</td>
                <td style={{ padding: '0.6rem', display: 'flex', gap: '0.5rem' }}>
                  <button onClick={() => handleDismissReport(rep.id)} style={{
                    background: '#6b7280', color: 'white', border: 'none',
                    padding: '0.3rem 0.7rem', borderRadius: '4px', cursor: 'pointer', fontSize: '12px'
                  }}>Ignoră</button>
                  <button onClick={() => handleDeleteReview(rep.review_id, rep.id)} style={{
                    background: '#dc2626', color: 'white', border: 'none',
                    padding: '0.3rem 0.7rem', borderRadius: '4px', cursor: 'pointer', fontSize: '12px'
                  }}>Șterge recenzia</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Tabel locații */}
      <h2 style={{ color: 'black' }}>📍 Toate locațiile ({locations.length})</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
        <thead>
          <tr style={{ background: '#f3f4f6' }}>
            {['ID', 'Nume', 'Categorie', 'Rating', 'Verificat', 'Acțiuni'].map(h => (
              <th key={h} style={{ padding: '0.6rem', textAlign: 'left', borderBottom: '1px solid #e5e7eb', color: 'black' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {locations.map(loc => (
            <tr key={loc.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
              <td style={{ padding: '0.6rem' ,color: 'black'}}>{loc.id}</td>
              <td style={{ padding: '0.6rem',color: 'black' }}>{loc.name}</td>
              <td style={{ padding: '0.6rem',color: 'black' }}>{loc.category}</td>
              <td style={{ padding: '0.6rem',color: 'black' }}>⭐ {loc.rating_avg}</td>
              <td style={{ padding: '0.6rem' }}>{loc.is_verified ? '✅' : '❌'}</td>
              <td style={{ padding: '0.6rem', display: 'flex', gap: '0.5rem' }}>
                {!loc.is_verified && (
                  <button onClick={() => handleApprove(loc.id)} style={{
                    background: '#16a34a', color: 'white', border: 'none',
                    padding: '0.3rem 0.7rem', borderRadius: '4px', cursor: 'pointer', fontSize: '12px'
                  }}>Approve</button>
                )}
                <button onClick={() => handleDelete(loc.id)} style={{
                  background: '#dc2626', color: 'white', border: 'none',
                  padding: '0.3rem 0.7rem', borderRadius: '4px', cursor: 'pointer', fontSize: '12px'
                }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}