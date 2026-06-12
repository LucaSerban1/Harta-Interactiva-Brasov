# Documentația AI — Ghidul AI local

Acest document descrie funcționalitatea AI integrată în aplicație: arhitectura, endpoint-urile, prompt-urile folosite și limitările cunoscute.

## Prezentare generală

Aplicația include un **asistent conversațional** ("Ghid AI local") care:

1. **Recomandă locații** din Brașov pe baza datelor reale din baza de date (nu inventează locații)
2. **Identifică trasee** între două locații cerute de utilizator și returnează ID-urile lor pentru desenarea rutei pe hartă
3. **Adaugă locații noi din link-uri Google Maps** (funcționalitate disponibilă doar adminilor): extrage coordonatele și numele din link, iar AI-ul clasifică automat categoria și generează o descriere

## Arhitectură

```
┌──────────────┐   POST /api/ai/chat    ┌──────────────────┐   chat.completions   ┌─────────────┐
│ AIAssistant  │ ─────────────────────► │ backend          │ ───────────────────► │ Groq API    │
│ (React)      │ ◄───────────────────── │ routers/ai.py    │ ◄─────────────────── │ Llama 3.1   │
└──────────────┘     JSON structurat    └────────┬─────────┘      JSON object     └─────────────┘
                                                 │
                                                 ▼
                                        ┌──────────────────┐
                                        │ PostgreSQL       │
                                        │ (locații reale)  │
                                        └──────────────────┘
```

- **Furnizor:** [Groq](https://groq.com) — inferență rapidă, plan gratuit
- **Model:** `llama-3.1-8b-instant`
- **Fișier principal:** `backend/app/routers/ai.py`
- **Componentă frontend:** `frontend/src/components/AIAssistant.tsx`

## Endpoint

### `POST /api/ai/chat`

**Request:**

```json
{
  "messages": [
    { "role": "user", "content": "Recomandă-mi o cafenea liniștită pentru învățat" }
  ]
}
```

Întregul istoric al conversației este trimis la fiecare request (modelul nu are memorie între apeluri).

**Response (JSON structurat, impus prin `response_format: json_object`):**

```json
{
  "mesaj": "Îți recomand cafeneaua X...",
  "location_id": 12,
  "start_location_id": null,
  "refresh_locations": false
}
```

| Câmp | Semnificație |
|------|--------------|
| `mesaj` | Răspunsul conversațional afișat utilizatorului |
| `location_id` | ID-ul locației recomandate / destinației (harta face zoom pe ea) |
| `start_location_id` | ID-ul locației de start, dacă utilizatorul a cerut un traseu |
| `refresh_locations` | `true` dacă a fost adăugată o locație nouă și frontend-ul trebuie să reîncarce harta |

Autentificarea este **opțională** (`get_optional_user`): oricine poate conversa cu ghidul, dar adăugarea de locații din link Google Maps cere cont de admin.

## Grounding — cum evităm halucinațiile

La fiecare request, **toate locațiile din baza de date** sunt serializate compact (`id`, `nume`, `categorie`, `descriere`, `tags`) și injectate în system prompt. Modelul primește instrucțiunea să aleagă doar din aceste date și să returneze ID-uri numerice existente. Astfel:

- recomandările sunt întotdeauna locații reale de pe hartă;
- ID-urile returnate pot fi validate de frontend înainte de zoom/rută.

## Fluxul de adăugare a locațiilor din Google Maps

1. Backend-ul detectează cu regex link-uri `google.com/maps` sau `maps.app.goo.gl` în ultimul mesaj
2. Verifică drepturile: utilizator neautentificat sau non-admin → AI-ul este instruit (printr-un mesaj de sistem) să refuze politicos
3. Pentru admini: urmărește redirect-urile link-ului, extrage coordonatele (`@lat,lng`) și numele locației din URL sau din `<title>`
4. Llama 3.1 clasifică locația într-una din categoriile aplicației și generează o descriere scurtă în română (răspuns JSON strict)
5. Locația este creată în baza de date cu tag-ul `google_maps`, iar asistentul confirmă utilizatorului adăugarea

## Configurare

```env
GROQ_API_KEY=...   # backend/.env — obligatoriu pentru funcționalitatea AI
```

Dacă biblioteca `groq` nu este instalată sau cheia lipsește, endpoint-ul răspunde cu un mesaj de eroare prietenos, iar restul aplicației funcționează normal — funcționalitatea AI este complet decuplată.

## Limitări cunoscute

- **Context complet la fiecare apel:** toate locațiile sunt trimise în prompt la fiecare mesaj; la sute de locații, promptul poate depăși limita de context a modelului — ar fi nevoie de filtrare/căutare semantică prealabilă
- **Fără memorie server-side:** istoricul conversației trăiește doar în starea componentei React
- **Modelul poate greși ID-uri:** deși primește instrucțiuni stricte, un model de 8B poate returna ocazional `location_id` greșit; frontend-ul tratează ID-urile inexistente ca null
- **Extragerea numelui din Google Maps este euristică** (regex pe URL/titlu) și poate produce nume imprecise pentru link-uri scurte

## AI folosit în dezvoltare

Pe lângă AI-ul din aplicație, echipa a folosit agenți AI (Claude Code) în procesul de dezvoltare — evaluarea detaliată a acestora se găsește în [AGENTS_EVALUATION.md](AGENTS_EVALUATION.md).
