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

## Documentație

- [Documentația AI](docs/AI_DOCUMENTATION.md) — arhitectura și funcționarea Ghidului AI local (Groq / Llama 3.1)
- [Evaluarea agenților AI](docs/AGENTS_EVALUATION.md) — cum au fost folosiți și evaluați agenții AI (Claude Code) în dezvoltarea proiectului

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
# opțional — origin-urile permise de CORS, separate prin virgulă
# (default: http://localhost:5173,http://localhost)
CORS_ORIGINS=http://localhost:5173,http://localhost
```

Frontend-ul citește opțional `VITE_API_URL` (default `http://localhost:8000`) — URL-ul backend-ului, embedat în bundle la build.

## Diagrame UML

### Class Diagram — Modele

```mermaid
classDiagram
    class User {
        +int id
        +String email
        +String username
        +String hashed_password
        +Boolean is_active
        +Boolean is_admin
        +DateTime created_at
    }

    class Location {
        +int id
        +String name
        +Float lat
        +Float lng
        +String category
        +String description
        +Float rating_avg
        +Boolean is_verified
        +String[] tags
    }

    class Review {
        +int id
        +int location_id
        +int user_id
        +Float rating
        +String text
        +DateTime created_at
    }

    class Favorite {
        +int id
        +int user_id
        +int location_id
        +DateTime created_at
    }

    class ReviewReport {
        +int id
        +int review_id
        +int reporter_id
        +String reason
        +DateTime created_at
    }

    User "1" --> "0..*" Review : scrie
    User "1" --> "0..*" Favorite : salvează
    User "1" --> "0..*" ReviewReport : raportează
    Location "1" --> "0..*" Review : primește
    Location "1" --> "0..*" Favorite : apare în
    Review "1" --> "0..*" ReviewReport : este raportat prin
```

### Sequence Diagram — Autentificare Google OAuth

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant Backend
    participant Google
    participant DB

    User->>Frontend: Click "Login"
    Frontend->>Backend: GET /auth/login
    Backend-->>Frontend: Redirect → Google OAuth URL
    Frontend->>Google: Redirect cu client_id + scope
    User->>Google: Autentificare cu cont Google
    Google-->>Backend: Redirect /auth/callback?code=...
    Backend->>Google: POST /token (exchange code)
    Google-->>Backend: access_token
    Backend->>Google: GET /userinfo
    Google-->>Backend: email, name
    Backend->>DB: Caută user după email
    alt User nou
        DB-->>Backend: null
        Backend->>DB: INSERT user
    else User existent
        DB-->>Backend: User
    end
    Backend->>Backend: Generează JWT (24h)
    Backend-->>Frontend: Redirect /auth/callback?token=JWT
    Frontend->>Frontend: Salvează token în localStorage
    Frontend-->>User: Redirecționat la hartă
```

### ER Diagram — Baza de date

```mermaid
erDiagram
    users {
        int id PK
        string email
        string username
        string hashed_password
        boolean is_active
        boolean is_admin
        datetime created_at
    }

    locations {
        int id PK
        string name
        float lat
        float lng
        string category
        string description
        float rating_avg
        boolean is_verified
        string[] tags
    }

    reviews {
        int id PK
        int location_id FK
        int user_id FK
        float rating
        string text
        datetime created_at
    }

    favorites {
        int id PK
        int user_id FK
        int location_id FK
        datetime created_at
    }

    review_reports {
        int id PK
        int review_id FK
        int reporter_id FK
        string reason
        datetime created_at
    }

    users ||--o{ reviews : "scrie"
    users ||--o{ favorites : "salvează"
    users ||--o{ review_reports : "raportează"
    locations ||--o{ reviews : "primește"
    locations ||--o{ favorites : "apare în"
    reviews ||--o{ review_reports : "este raportat prin"
```

## CI/CD

- **CI** (`.github/workflows/ci.yml`) — la fiecare push/PR pe `develop`/`main`: teste backend (pytest + PostgreSQL), lint și build frontend
- **CD** (`.github/workflows/cd.yml`) — la fiecare push pe `develop`/`main`: construiește imaginile Docker pentru backend și frontend și le publică pe GitHub Container Registry

Imaginile publicate pot fi rulate direct:

```bash
docker pull ghcr.io/lucaserban1/harta-interactiva-brasov-backend:latest
docker pull ghcr.io/lucaserban1/harta-interactiva-brasov-frontend:latest
```

Pentru un alt mediu, imaginea de frontend se construiește cu URL-ul backend-ului dorit:

```bash
docker build --build-arg VITE_API_URL=https://api.example.com -t frontend ./frontend
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
