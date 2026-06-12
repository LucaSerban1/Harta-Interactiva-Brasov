# Evaluarea agenților AI folosiți în dezvoltare

Acest document evaluează agenții AI utilizați în dezvoltarea proiectului: ce sarcini au primit, cum s-au descurcat, unde a fost nevoie de intervenție umană și ce concluzii am tras.

## Agenți folosiți

| Agent | Model(e) | Rol în proiect |
|-------|----------|----------------|
| **Claude Code** (CLI) | Claude Sonnet 4.6, Claude Fable 5 | Agent principal: implementare funcționalități, CI/CD, fix-uri, code review, documentație |
| **Subagenți Claude Code** (`Explore`) | Sonnet | Căutare paralelă de bug-uri în code review (analiza pe unghiuri multiple) |

## Sarcini date agenților și rezultate

### 1. Configurarea CI (GitHub Actions)

**Sarcina:** workflow de CI cu teste backend (pytest + PostgreSQL ca service container), lint și build frontend.

**Rezultat:** workflow-ul final funcționează, dar a necesitat **4 iterații de fix-uri** vizibile în istoricul git:

- `f4edfc5` — `DATABASE_URL` greșit pentru alembic + versiune de Node prea veche (18 → 20)
- `33d9600` — importuri greșite în `seed.py`, erori de eslint, variabilă nefolosită
- `6c3e876` — variabilă de `catch` nefolosită (regula `no-unused-vars`)
- `aa9b143` — erori de tip TypeScript în `AIAssistant` și tipul `AIResponse`

**Evaluare:** agentul a produs rapid scheletul corect, dar nu a anticipat diferențele dintre mediul local și runner-ul de CI (versiuni, variabile de mediu). Iterațiile au fost însă rapide — fiecare fix a durat minute, ghidat de log-urile de CI.

### 2. Pipeline-ul de CD (PR [#31](https://github.com/LucaSerban1/Harta-Interactiva-Brasov/pull/31))

**Sarcina:** Dockerfile-uri pentru backend și frontend + workflow de publicare automată a imaginilor pe GitHub Container Registry.

**Rezultat:** implementare funcțională din prima iterație de cod, dar **code review-ul automat a găsit 3 probleme majore** în propria implementare a agentului (vezi secțiunea următoare), corectate apoi într-un commit de follow-up (`1f615d7`).

**Evaluare:** un exemplu bun de "AI care scrie + AI care verifică" — prima versiune era plauzibilă și ar fi trecut neobservată la o citire superficială, dar avea lacune reale de deployment (migrații nerulate, lipsa gating-ului pe CI).

### 3. Code review automat (PR #31)

**Sarcina:** review de tip "recall ridicat": 7 unghiuri de analiză rulate de subagenți paraleli → 12 candidați de bug-uri → verificare individuală → constatări finale postate ca review comments pe PR.

**Rezultat:**

| Metrică | Valoare |
|---------|---------|
| Candidați găsiți de subagenți | 12 |
| Constatări confirmate/plauzibile | 5 (3 majore, 2 minore) |
| Falsuri pozitive respinse la verificare | 2 |
| Constatări transformate în issue-uri | 1 ([#32](https://github.com/LucaSerban1/Harta-Interactiva-Brasov/issues/32)) |

Exemple de constatări reale: CD-ul publica imagini chiar dacă testele picau; containerul de backend nu rula migrațiile alembic; bundle-ul de frontend embedează URL-ul API hardcodat.

Exemple de falsuri pozitive respinse: un subagent a susținut că `IMAGE_PREFIX` conține majuscule și GHCR îl va respinge — fals, valoarea era deja lowercase (halucinație tipică: agentul a confundat numele repo-ului cu valoarea variabilei).

**Evaluare:** pasul de **verificare** este esențial — fără el, ~17% din constatări ar fi fost zgomot. Cu verificare, review-ul a găsit probleme pe care autorii (om + AI) le rataseră.

### 4. Documentație și diagrame UML

**Sarcina:** README, diagrame Mermaid (class, sequence, ER), documentația AI.

**Rezultat:** corect din prima în mare parte; diagramele au necesitat doar ajustări mici de sintaxă Mermaid. Agentul a citit codul real (modele SQLAlchemy, router-ul de auth) înainte de a desena diagramele, deci ele reflectă schema reală, nu una inventată.

## Criterii de evaluare și scoruri

| Criteriu | Scor (1–5) | Observații |
|----------|-----------|------------|
| **Corectitudinea codului generat** | 4 | Codul compilează și funcționează aproape întotdeauna local; problemele apar la marginile sistemului (CI, deployment, configurare) |
| **Autonomie** | 4 | Poate duce singur un flux complet issue → branch → PR → review → merge; cere confirmare la deciziile de arhitectură |
| **Viteză** | 5 | Sarcini care ar dura ore (CD pipeline complet + docs) se termină în minute |
| **Anticiparea mediului de producție** | 3 | Punctul cel mai slab: diferențele local vs. CI vs. container au necesitat iterații |
| **Calitatea review-ului de cod** | 4 | Găsește bug-uri reale ratate de oameni, dar produce și falsuri pozitive — necesită pas de verificare |
| **Documentație** | 5 | Documentația generată e ancorată în codul real, nu generică |

## Concluzii

1. **AI-ul nu înlocuiește review-ul, îl alimentează.** Cele mai valoroase rezultate au venit din combinația *agent care scrie* + *agent care verifică* + *om care decide* — review-ul automat a găsit bug-uri reale în cod scris tot de AI.
2. **Log-urile de CI sunt cel mai bun feedback pentru agent.** Toate cele 4 iterații de fix CI au fost rezolvate rapid pentru că agentul a primit log-ul exact al erorii.
3. **Verificarea umană rămâne obligatorie la marginile sistemului:** secrete, variabile de mediu, drepturi pe registry, comportament în producție.
4. **Falsurile pozitive sunt gestionabile** dacă fluxul include un pas explicit de verificare a fiecărei constatări înainte de raportare.
