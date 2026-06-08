import { useState, useEffect } from 'react';
import type { Location } from '../mockData';
import { fetchReviewsByLocation, reportReview, checkFavorite, addFavorite, removeFavorite } from '../api';

interface ApiReview {
  id: number;
  user_id: number;
  rating: number;
  text: string;
  created_at: string;
  user?: { id: number; username: string; is_admin: boolean };
}

interface Props {
  location: Location;
  onClose: () => void;
}

export default function LocationPanel({ location, onClose }: Props) {
  const [photoIndex, setPhotoIndex] = useState(0);
  const [reviews, setReviews] = useState<ApiReview[]>([]);
  const [reportingId, setReportingId] = useState<number | null>(null);
  const [reason, setReason] = useState('');
  const [msg, setMsg] = useState('');
  const [isFavorite, setIsFavorite] = useState(false);
  const [favLoading, setFavLoading] = useState(false);

  const photos = location.photos ?? [];
  const rating = location.rating_avg ?? location.rating ?? 0;

  const currentUserId = (() => {
    const token = localStorage.getItem('token');
    if (!token) return null;
    try {
      return parseInt(JSON.parse(atob(token.split('.')[1])).sub);
    } catch { return null; }
  })();

  useEffect(() => {
    setReviews([]);
    setReportingId(null);
    setReason('');
    setMsg('');
    fetchReviewsByLocation(location.id).then(setReviews).catch(() => {});
    checkFavorite(location.id).then(setIsFavorite);
  }, [location.id]);

  const handleToggleFavorite = async () => {
    const token = localStorage.getItem('token');
    if (!token) { setMsg('Trebuie să fii logat pentru a adăuga la favorite.'); return; }
    setFavLoading(true);
    if (isFavorite) {
      await removeFavorite(location.id);
      setIsFavorite(false);
    } else {
      await addFavorite(location.id);
      setIsFavorite(true);
    }
    setFavLoading(false);
  };

  const handleReport = async (reviewId: number) => {
    if (!reason.trim()) return;
    const token = localStorage.getItem('token');
    if (!token) {
      setMsg('Trebuie să fii logat pentru a raporta.');
      return;
    }
    const res = await reportReview(reviewId, reason.trim());
    if (res.status === 201) {
      setMsg('Recenzie raportată cu succes!');
      setReportingId(null);
      setReason('');
    } else if (res.status === 409) {
      setMsg('Ai raportat deja această recenzie.');
      setReportingId(null);
    } else if (res.status === 400) {
      setMsg('Nu poți raporta propria recenzie.');
      setReportingId(null);
    } else if (res.status === 401) {
      setMsg('Trebuie să fii logat pentru a raporta.');
      setReportingId(null);
    } else {
      setMsg('Eroare la raportare.');
    }
  };

  return (
    <div style={{
      position: 'fixed', top: 0, right: 0, width: '360px', height: '100vh',
      background: 'white', zIndex: 1000, overflowY: 'auto',
      boxShadow: '-2px 0 8px rgba(0,0,0,0.2)', padding: '1rem',
      color: 'black'
    }}>
      <button onClick={onClose} style={{ float: 'right', cursor: 'pointer' }}>✕</button>

      <h2 style={{ marginTop: 0, color: 'black' }}>{location.name}</h2>
      {location.address && <p style={{ color: '#666' }}>{location.address}</p>}
      {location.description && <p style={{ color: '#444' }}>{location.description}</p>}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
        <p style={{ margin: 0 }}>⭐ {rating} · <span style={{ color: '#888' }}>{location.category}</span></p>
        <button
          onClick={handleToggleFavorite}
          disabled={favLoading}
          style={{
            background: isFavorite ? '#fee2e2' : '#f3f4f6',
            color: isFavorite ? '#dc2626' : '#555',
            border: 'none', borderRadius: '20px',
            padding: '0.3rem 0.8rem', cursor: 'pointer',
            fontSize: '13px', fontWeight: 500,
            transition: 'all 0.2s'
          }}
        >
          {isFavorite ? '❤️ Favorit' : '🤍 Adaugă la favorite'}
        </button>
      </div>

      {location.tags && (
        <div style={{ marginBottom: '1rem' }}>
          {location.tags.map(tag => (
            <span key={tag} style={{
              display: 'inline-block', background: '#f0f0f0',
              borderRadius: '12px', padding: '2px 10px',
              fontSize: '12px', marginRight: '4px', marginBottom: '4px'
            }}>#{tag}</span>
          ))}
        </div>
      )}

      {photos.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <img src={photos[photoIndex]} alt="foto" style={{ width: '100%', borderRadius: '8px' }} />
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem' }}>
            <button onClick={() => setPhotoIndex(i => Math.max(0, i - 1))} disabled={photoIndex === 0}>◀ Prev</button>
            <span>{photoIndex + 1} / {photos.length}</span>
            <button onClick={() => setPhotoIndex(i => Math.min(photos.length - 1, i + 1))} disabled={photoIndex === photos.length - 1}>Next ▶</button>
          </div>
        </div>
      )}

      <h3>Review-uri</h3>
      {msg && (
        <p style={{ fontSize: '13px', color: msg.includes('succes') ? 'green' : 'red', marginBottom: '0.5rem' }}>{msg}</p>
      )}
      {reviews.length === 0 ? (
        <p style={{ color: '#000' }}>Nu există review-uri încă.</p>
      ) : (
        reviews.slice(0, 10).map(review => (
          <div key={review.id} style={{
            borderTop: '1px solid #eee', paddingTop: '0.5rem', marginTop: '0.5rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <strong>{review.user?.username ?? `User #${review.user_id}`}</strong>
              <span>⭐ {review.rating}</span>
            </div>
            <p style={{ margin: '4px 0', color: 'black' }}>{review.text}</p>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <small style={{ color: '#aaa' }}>{new Date(review.created_at).toLocaleDateString('ro-RO')}</small>
              {currentUserId !== review.user_id && (
                <button
                  onClick={() => { setReportingId(review.id); setReason(''); setMsg(''); }}
                  style={{
                    background: 'none', border: 'none', cursor: 'pointer',
                    color: '#dc2626', fontSize: '12px', padding: '2px 6px'
                  }}
                >🚩 Raportează</button>
              )}
            </div>

            {reportingId === review.id && (
              <div style={{ marginTop: '0.5rem', background: '#fef2f2', borderRadius: '8px', padding: '0.75rem' }}>
                <p style={{ margin: '0 0 0.4rem', fontSize: '13px', color: '#7f1d1d', fontWeight: 600 }}>Motiv raportare:</p>
                <textarea
                  value={reason}
                  onChange={e => setReason(e.target.value)}
                  placeholder="Descrie de ce raportezi această recenzie..."
                  style={{
                    width: '100%', height: '70px', resize: 'none', borderRadius: '6px',
                    border: '1px solid #fca5a5', padding: '0.4rem', fontSize: '13px',
                    boxSizing: 'border-box'
                  }}
                />
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.4rem' }}>
                  <button
                    onClick={() => handleReport(review.id)}
                    disabled={!reason.trim()}
                    style={{
                      flex: 1, background: '#dc2626', color: 'white', border: 'none',
                      borderRadius: '6px', padding: '0.4rem', cursor: 'pointer', fontSize: '13px'
                    }}
                  >Trimite raport</button>
                  <button
                    onClick={() => { setReportingId(null); setReason(''); }}
                    style={{
                      flex: 1, background: '#e5e7eb', color: '#333', border: 'none',
                      borderRadius: '6px', padding: '0.4rem', cursor: 'pointer', fontSize: '13px'
                    }}
                  >Anulează</button>
                </div>
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
}
