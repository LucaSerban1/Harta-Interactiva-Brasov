# Harta Interactivă Brașov

O aplicație web interactivă pentru explorarea orașului Brașov — locații, recenzii, favorite și un ghid AI local.

## Tehnologii

**Frontend:** React 19, TypeScript, Vite, React-Leaflet  
**Backend:** FastAPI, SQLAlchemy, PostgreSQL, Alembic  
**AI:** Groq API (Llama 3.1)  
**Auth:** Google OAuth 2.0 + JWT

## Funcționalități

- **Hartă interactivă** cu locații din Brașov (cafenele, parcuri, restaurante, obiective turistice etc.)
- **Filtrare și căutare** după nume, categorie sau taguri
- **Recenzii** — adaugă, vizualizează și șterge recenzii cu rating
- **Raportare recenzii** — raportează conținut nepotrivit; adminii pot gestiona rapoartele
- **Favorite** — salvează locații preferate și le vizualizezi în profilul tău
- **Istoric recenzii** — vezi toate recenziile scrise de tine
- **Ghid AI local** — asistent conversațional care recomandă locații, trasee și poate adăuga locații noi prin link Google Maps (doar admini)
- **Admin Panel** — gestionează locații, aprobă, șterge și moderează rapoarte
- **Autentificare Google** — login cu cont Google

## Rulare locală

### Cerințe
- Docker Desktop
- Node.js 18+
- Python 3.11+

### 1. Baza de date
```bash
docker compose up -d
```

### 2. Backend
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Backend disponibil la `http://localhost:8000`  
Documentație API: `http://localhost:8000/docs`

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend disponibil la `http://localhost:5173`

### 4. Variabile de mediu

Creează fișierul `backend/.env`:

```env
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
SECRET_KEY=...
GROQ_API_KEY=...
ALLOWED_DOMAINS=gmail.com,s.unibuc.ro,unibuc.ro
```

## Structura proiectului

```
├── backend/
│   ├── app/
│   │   ├── models/        # Modele SQLAlchemy
│   │   ├── schemas/       # Scheme Pydantic
│   │   ├── crud/          # Logică acces date
│   │   ├── routers/       # Endpoint-uri FastAPI
│   │   └── main.py
│   ├── alembic/           # Migrații bază de date
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/    # MapView, LocationPanel, AIAssistant etc.
│       ├── pages/         # ProfilePage, AdminPage, AuthCallback
│       └── api.ts
└── docker-compose.yml
```
