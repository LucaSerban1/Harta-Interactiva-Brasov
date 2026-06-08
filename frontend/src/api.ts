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

export interface AIResponse {
  mesaj?: string;
  location_id?: number | null;
  start_location_id?: number | null;
  eroare_detaliata?: string;
  error?: string;
}

export async function fetchAIRecommendation(prompt: string): Promise<AIResponse> {
  const res = await fetch(`${BASE_URL}/api/ai/recommend?prompt_user=${encodeURIComponent(prompt)}`);
  if (!res.ok) throw new Error('Eroare la conectarea cu AI-ul');
  return res.json();
}

export async function sendChatMessage(messages: {role: string, content: string}[]): Promise<AIResponse> {
  const res = await fetch(`${BASE_URL}/api/ai/chat`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ messages })
  });
  if (!res.ok) throw new Error('Eroare la conectarea cu AI-ul');
  return res.json();
}

export async function checkFavorite(locationId: number): Promise<boolean> {
  const token = localStorage.getItem('token');
  if (!token) return false;
  const res = await fetch(`${BASE_URL}/favorites/check/${locationId}`, { headers: getHeaders() });
  if (!res.ok) return false;
  const data = await res.json();
  return data.is_favorite;
}

export async function addFavorite(locationId: number) {
  return fetch(`${BASE_URL}/favorites/${locationId}`, { method: 'POST', headers: getHeaders() });
}

export async function removeFavorite(locationId: number) {
  return fetch(`${BASE_URL}/favorites/${locationId}`, { method: 'DELETE', headers: getHeaders() });
}

export async function fetchReviewsByLocation(locationId: number) {
  const res = await fetch(`${BASE_URL}/reviews/${locationId}`, {
    headers: getHeaders()
  });
  if (!res.ok) throw new Error('Eroare la fetch reviews');
  return res.json();
}

export async function reportReview(reviewId: number, reason: string) {
  const res = await fetch(`${BASE_URL}/reviews/${reviewId}/report`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ reason })
  });
  return res;
}