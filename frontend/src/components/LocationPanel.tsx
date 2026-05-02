import { useState } from 'react';
import type { Location } from '../mockData';

interface Props {
  location: Location;
  onClose: () => void;
}

export default function LocationPanel({ location, onClose }: Props) {
  const [photoIndex, setPhotoIndex] = useState(0);

  return (
    <div style={{
      position: 'absolute', top: 0, right: 0, width: '360px', height: '100vh',
      background: 'white', zIndex: 1000, overflowY: 'auto',
      boxShadow: '-2px 0 8px rgba(0,0,0,0.2)', padding: '1rem'
    }}>
      <button onClick={onClose} style={{ float: 'right', cursor: 'pointer' }}>✕</button>

      <h2>{location.name}</h2>
      <p style={{ color: '#666' }}>{location.address}</p>
      <p>⭐ {location.rating} · <span style={{ color: '#888' }}>{location.category}</span></p>

      {/* Carusel poze */}
      <div style={{ position: 'relative', marginBottom: '1rem' }}>
        <img
          src={location.photos[photoIndex]}
          alt="foto"
          style={{ width: '100%', borderRadius: '8px' }}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem' }}>
          <button
            onClick={() => setPhotoIndex(i => Math.max(0, i - 1))}
            disabled={photoIndex === 0}
          >◀ Prev</button>
          <span>{photoIndex + 1} / {location.photos.length}</span>
          <button
            onClick={() => setPhotoIndex(i => Math.min(location.photos.length - 1, i + 1))}
            disabled={photoIndex === location.photos.length - 1}
          >Next ▶</button>
        </div>
      </div>

      {/* Review-uri */}
      <h3>Review-uri</h3>
      {location.reviews.slice(0, 10).map(review => (
        <div key={review.id} style={{
          borderTop: '1px solid #eee', paddingTop: '0.5rem', marginTop: '0.5rem'
        }}>
          <strong>{review.user}</strong> — ⭐ {review.rating}
          <p style={{ margin: '4px 0' }}>{review.text}</p>
          <small style={{ color: '#aaa' }}>{review.date}</small>
        </div>
      ))}
    </div>
  );
}