interface Props {
  value: string;
  onChange: (val: string) => void;
}

export default function SearchBar({ value, onChange }: Props) {
  return (
    <input
      type="text"
      placeholder="Caută locație... (ex: cafea, study)"
      value={value}
      onChange={e => onChange(e.target.value)}
      style={{
  position: 'fixed', top: '1rem', left: '50%',
  transform: 'translateX(-50%)',
  zIndex: 9999, width: '320px', padding: '0.6rem 1rem',
  borderRadius: '8px', border: '1px solid #ccc',
  boxShadow: '0 2px 6px rgba(0,0,0,0.2)', fontSize: '14px',
  background: 'white', color: 'black'
}}
    />
  );
}