# AI Documentation — Local AI Guide

This document describes the AI functionality built into the application: architecture, endpoints, the prompts used and known limitations.

## Overview

The application includes a **conversational assistant** ("Local AI Guide") that:

1. **Recommends locations** in Brașov based on real data from the database (it does not make up locations)
2. **Identifies routes** between two locations requested by the user and returns their IDs so the route can be drawn on the map
3. **Adds new locations from Google Maps links** (admin-only feature): it extracts the coordinates and name from the link, then the AI automatically classifies the category and generates a description

## Architecture

```
┌──────────────┐   POST /api/ai/chat    ┌──────────────────┐   chat.completions   ┌─────────────┐
│ AIAssistant  │ ─────────────────────► │ backend          │ ───────────────────► │ Groq API    │
│ (React)      │ ◄───────────────────── │ routers/ai.py    │ ◄─────────────────── │ Llama 3.1   │
└──────────────┘     structured JSON    └────────┬─────────┘      JSON object     └─────────────┘
                                                 │
                                                 ▼
                                        ┌──────────────────┐
                                        │ PostgreSQL       │
                                        │ (real locations) │
                                        └──────────────────┘
```

- **Provider:** [Groq](https://groq.com) — fast inference, free tier
- **Model:** `llama-3.1-8b-instant`
- **Main file:** `backend/app/routers/ai.py`
- **Frontend component:** `frontend/src/components/AIAssistant.tsx`

## Endpoint

### `POST /api/ai/chat`

**Request:**

```json
{
  "messages": [
    { "role": "user", "content": "Recommend a quiet café for studying" }
  ]
}
```

The entire conversation history is sent with every request (the model has no memory between calls).

**Response (structured JSON, enforced via `response_format: json_object`):**

```json
{
  "mesaj": "I recommend café X...",
  "location_id": 12,
  "start_location_id": null,
  "refresh_locations": false
}
```

| Field | Meaning |
|------|--------------|
| `mesaj` | The conversational answer shown to the user |
| `location_id` | ID of the recommended location / destination (the map zooms to it) |
| `start_location_id` | ID of the starting location, if the user asked for a route |
| `refresh_locations` | `true` if a new location was added and the frontend should reload the map |

Authentication is **optional** (`get_optional_user`): anyone can chat with the guide, but adding locations from a Google Maps link requires an admin account.

## Grounding — how we avoid hallucinations

On every request, **all locations from the database** are serialized compactly (`id`, `name`, `category`, `description`, `tags`) and injected into the system prompt. The model is instructed to choose only from this data and to return existing numeric IDs. As a result:

- recommendations are always real locations that exist on the map;
- the returned IDs can be validated by the frontend before zooming/routing.

## Google Maps location-adding flow

1. The backend detects `google.com/maps` or `maps.app.goo.gl` links in the last message using a regex
2. It checks permissions: unauthenticated or non-admin user → the AI is instructed (via a system message) to politely refuse
3. For admins: it follows the link's redirects, extracts the coordinates (`@lat,lng`) and the location name from the URL or from the `<title>`
4. Llama 3.1 classifies the location into one of the app's categories and generates a short description (strict JSON response)
5. The location is created in the database with the `google_maps` tag, and the assistant confirms the addition to the user

## Configuration

```env
GROQ_API_KEY=...   # backend/.env — required for the AI functionality
```

If the `groq` library is not installed or the key is missing, the endpoint responds with a friendly error message and the rest of the application works normally — the AI functionality is fully decoupled.

## Known limitations

- **Full context on every call:** all locations are sent in the prompt with every message; with hundreds of locations the prompt could exceed the model's context limit — pre-filtering / semantic search would be needed
- **No server-side memory:** the conversation history lives only in the React component state
- **The model can get IDs wrong:** despite strict instructions, an 8B model may occasionally return a wrong `location_id`; the frontend treats non-existent IDs as null
- **Google Maps name extraction is heuristic** (regex over URL/title) and may produce imprecise names for short links
- **The assistant converses in Romanian** — the system prompt and the in-app audience are Romanian-speaking by design

## AI used during development

Besides the in-app AI, the team used AI agents (Claude Code) during the development process — their detailed evaluation can be found in [AGENTS_EVALUATION.md](AGENTS_EVALUATION.md).
