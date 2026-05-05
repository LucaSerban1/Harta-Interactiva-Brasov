import { useState } from 'react';
import type { Location } from '../mockData';

interface Props {
  location: Location;
  onClose: () => void;
}

export default function LocationPanel({ location, onClose }: Props) {
  const [photoIndex, setPhotoIndex] = useState(0);
  const photos = location.photos ?? [];
  const reviews = location.reviews ?? [];
  const rating = location.rating_avg ?? location.rating ?? 0;

  return (
    <div style={{
      position: 'fixed', top: 0, right: 0, width: '360px', height: '100vh',
      background: 'white', zIndex: 1000, overflowY: 'auto',
      boxShadow: '-2px 0 8px rgba(0,0,0,0.2)', padding: '1rem',
      color: 'black'
    }}>
      <button onClick={onClose} style={{ float: 'right', cursor: 'pointer' }}>✕</button>

      <h2 style={{ marginTop: 0 }}>{location.name}</h2>
      {location.address && <p style={{ color: '#666' }}>{location.address}</p>}
      {location.description && <p style={{ color: '#444' }}>{location.description}</p>}
      <p>⭐ {rating} · <span style={{ color: '#888' }}>{location.category}</span></p>

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
          <img
            src={photos[photoIndex]}
            alt="foto"
            style={{ width: '100%', borderRadius: '8px' }}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem' }}>
            <button onClick={() => setPhotoIndex(i => Math.max(0, i - 1))} disabled={photoIndex === 0}>◀ Prev</button>
            <span>{photoIndex + 1} / {photos.length}</span>
            <button onClick={() => setPhotoIndex(i => Math.min(photos.length - 1, i + 1))} disabled={photoIndex === photos.length - 1}>Next ▶</button>
          </div>
        </div>
      )}

      <h3>Review-uri</h3>
      {reviews.length === 0 ? (
        <p style={{ color: '#aaa' }}>Nu există review-uri încă.</p>
      ) : (
        reviews.slice(0, 10).map(review => (
          <div key={review.id} style={{
            borderTop: '1px solid #eee', paddingTop: '0.5rem', marginTop: '0.5rem'
          }}>
            <strong>{review.user}</strong> — ⭐ {review.rating}
            <p style={{ margin: '4px 0' }}>{review.text}</p>
            <small style={{ color: '#aaa' }}>{review.date}</small>
          </div>
        ))
      )}
    </div>
  );
} 