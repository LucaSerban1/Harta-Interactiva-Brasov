const BASE_URL = 'http://localhost:8000';

function getHeaders() {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
}

export async function fetchLocations() {
  const res = await fetch(`${BASE_URL}/locations/`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Eroare la fetch locations');
  return res.json();
}

export async function fetchLocationById(id: number) {
  const res = await fetch(`${BASE_URL}/locations/${id}`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Eroare la fetch location');
  return res.json();
}

export async function fetchAIRecommendation(prompt: string) {
  const res = await fetch(`${BASE_URL}/api/ai/recommend?prompt_user=${encodeURIComponent(prompt)}`);
  if (!res.ok) throw new Error('Eroare la conectarea cu AI-ul');
  return res.json();
}