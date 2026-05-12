import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface User {
  id: number;
  email: string;
  username: string;
  is_admin: boolean;
}

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }
    fetch('http://localhost:8000/auth/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(r => r.json())
      .then(data => setUser(data))
      .catch(() => setError('Nu s-a putut încărca profilul'));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  if (error) return <p style={{ padding: '2rem', color: 'red' }}>{error}</p>;
  if (!user) return <p style={{ padding: '2rem' }}>Se încarcă...</p>;

  return (
    <div style={{
      minHeight: '100vh', background: 'white', display: 'flex',
      alignItems: 'center', justifyContent: 'center'
    }}>
      <div style={{
        background: '#f9f9f9', borderRadius: '16px', padding: '2rem',
        width: '360px', boxShadow: '0 4px 20px rgba(0,0,0,0.1)', color: 'black'
      }}>
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <div style={{
            width: '72px', height: '72px', borderRadius: '50%',
            background: '#2563eb', color: 'white', fontSize: '2rem',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 1rem'
          }}>
            {user.username[0].toUpperCase()}
          </div>
          <h2 style={{ margin: 0 }}>{user.username}</h2>
          <p style={{ color: '#666', marginTop: '0.25rem' }}>{user.email}</p>
          {user.is_admin && (
            <span style={{
              background: '#fef3c7', color: '#92400e', fontSize: '12px',
              padding: '2px 10px', borderRadius: '20px', marginTop: '0.5rem',
              display: 'inline-block'
            }}>👑 Admin</span>
          )}
        </div>

        <div style={{ borderTop: '1px solid #e5e7eb', paddingTop: '1rem' }}>
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
      </div>
    </div>
  );
}