interface Props {
  selected: string;
  onChange: (cat: string) => void;
}

const categories = [
  { value: '', label: '🗺️ Toate' },
  { value: 'cafe', label: '☕ Cafenele' },
  { value: 'library', label: '📚 Biblioteci' },
  { value: 'park', label: '🌳 Parcuri' },
  { value: 'study', label: '💻 Study/Cowork' },
  { value: 'restaurant', label: '🍽️ Restaurante' },
  { value: 'landmark', label: '🏛️ Obiective' },
];

export default function FilterBar({ selected, onChange }: Props) {
  return (
    <div style={{
      position: 'fixed', top: '4rem', left: '50%',
      transform: 'translateX(-50%)',
      zIndex: 9999, display: 'flex', gap: '0.5rem',
      background: 'white', padding: '0.5rem 0.75rem',
      borderRadius: '8px', boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
    }}>
      {categories.map(cat => (
        <button
          key={cat.value}
          onClick={() => onChange(cat.value)}
          style={{
            padding: '0.3rem 0.75rem', borderRadius: '20px', cursor: 'pointer',
            border: '1px solid #ccc', fontSize: '13px',
            background: selected === cat.value ? '#2563eb' : 'white',
            color: selected === cat.value ? 'white' : 'black',
          }}
        >
          {cat.label}
        </button>
      ))}
    </div>
  );
}