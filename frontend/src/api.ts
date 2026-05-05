const BASE_URL = 'http://localhost:8000';

export async function fetchLocations() {
  const res = await fetch(`${BASE_URL}/locations/`);
  if (!res.ok) throw new Error('Eroare la fetch locations');
  return res.json();
}

export async function fetchLocationById(id: number) {
  const res = await fetch(`${BASE_URL}/locations/${id}`);
  if (!res.ok) throw new Error('Eroare la fetch location');
  return res.json();
}