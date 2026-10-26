# Fișa de direcție — Harta Interactivă Brașov

| Echipa | Echipa-38 |
|---|---|
| Membri | Ardeleanu-Chirica Matei; Dumitrascu Ioan-Darius; Fuciuc Filip Luca; Serban Luca-Eugen |
| Repo | https://github.com/lucaserban1/harta-interactiva-brasov |

## 1. Sistemul, așa cum e acum (as-is)

- Hartă web a Brașovului: locații pe categorii, căutare/filtre, recenzii, favorite, raportare recenzii.
- Login Google OAuth → JWT 24h; admin = email `@unibuc.ro`, restul sunt useri obișnuiți.
- Ghid AI (Groq, Llama 3.1): recomandări și trasee; adminii adaugă locații dintr-un link Google Maps.
- Stack: React + Vite + Leaflet / FastAPI + PostgreSQL + Alembic; CI (teste, lint, build) și imagini Docker pe GHCR.
- Lipsuri: `POST/PATCH/DELETE /locations` fără autentificare; roluri doar după domeniul de email; fără hosting; 12 teste, doar pe locații și recenzii.

## 2. Direcția (to-be)

| # | Obiectiv | De ce acum | Cum știm că l-am atins |
|---|---|---|---|
| O1 | API securizat + roluri în DB (user, business, admin) | Azi oricine poate modifica locații; O2 are nevoie de un rol nou | Teste 401/403 pentru fiecare rol pe fiecare endpoint de scriere |
| O2 | Localurile își publică promoțiile, userii le văd pe hartă | Stakeholder nou (localuri) + motiv pentru useri să revină | Un cont business aprobat publică o promoție → apare pe hartă și în panou → dispare singură la expirare |
| O3 | Aplicația e online | Promoțiile au sens doar dacă le vede cineva | URL public funcțional, deploy automat din `develop` |

**Ce nu facem:** plăți, cupoane/QR validate în local, statistici pentru business, login cu email și parolă, aplicație mobilă, alte orașe.

## 3. Stakeholderii

| Cine | Ce vrea de la sistem | Cum aflăm ce vrea |
|---|---|---|
| Proprietari / manageri de localuri | Vizibilitate, pus o promoție rapid, fără efort tehnic | Interviu cu 2–3 cafenele/restaurante din Brașov |
| Studenți | Locuri de studiu/cafenele, oferte, recenzii de încredere | Interviu cu 3–5 colegi |
| Turiști / vizitatori | Recomandări, trasee, oferte la îndemână, fără cont | Scenariu de utilizare |
| Admini | Aprobare simplă a conturilor business, moderare | Observație pe pagina de admin |

## 4. Resursele noastre

| Resursă | Ce avem, realist | Ce ne lipsește |
|---|---|---|
| Oameni | 4 membri × ~5 ore/săptămână fiecare (~20 ore/săptămână în total) | Capacitate redusă în sesiunea de examene (ianuarie–februarie) și în săptămânile cu parțiale |
| Cunoștințe | React, FastAPI, SQL, Docker, CI, OAuth | Autorizare pe roluri, hosting în producție (prima dată) |
| Tehnice | GitHub Actions, GHCR, Postgres în Docker, Groq, Google OAuth | Mediu de hosting |
| Financiare | 0 lei — doar planuri gratuite (Groq, GHCR) | Buget, dacă hostingul gratuit nu ajunge |
| Acces la AI | Groq free tier în produs (limită tokeni/minut) | Nu punem în model: `.env`, chei, tokenuri, emailuri sau date ale userilor/localurilor |

## 5. Fezabilitate

| Întrebare | Da / Nu / Nu știm | De ce |
|---|---|---|
| Contribuie direcția la ce vor stakeholderii de la secțiunea 3? | Da | Localurile primesc vizibilitate, userii primesc oferte, adminii controlează cine publică |
| Se poate face până la final de semestru, cu resursele de la secțiunea 4? | Da, dacă ținem versiunea minimă | Un model nou + un rol nou + câteva pagini; hostingul e singura necunoscută |
| Se integrează cu ce există deja în sistem și în jurul lui? | Da | Promoția aparține unei `Location`; refolosim login-ul Google, routerele, CI/CD |

## 6. Primele cinci riscuri

Impact și probabilitate pe 1–3; scor = I × P.

| # | Risc | Tip | Impact | Prob. | Scor | Strategie |
|---|---|---|---|---|---|---|
| R1 | Un cont business modifică promoțiile altui local / oricine modifică locații | Securitate | 3 | 2 | 6 | Reducere: verificare de proprietar pe fiecare endpoint + teste (O1) |
| R2 | Niciun local real nu participă → nu avem confirmare și nici promoții la demo | Extern | 2 | 3 | 6 | Reducere: interviuri devreme; date demo în `seed.py` |
| R3 | Scope creep (QR, plăți, statistici) | Organizațional | 2 | 2 | 4 | Evitare: lista „Ce nu facem” |
| R4 | Membrii nu pot explica cod scris cu AI | Organizațional | 3 | 2 | 6 | Reducere: code review încrucișat, AI declarat în commit |
| R5 | Hostingul gratuit nu ajunge / OAuth greșit configurat în producție | Tehnic | 2 | 2 | 4 | Reducere: deploy devreme; plan B pe alt provider |

## 7. Cerințele candidate (după S4)

| # | Cerința | Prioritate | Tip | Sursa · confirmată de | De ce (rationale) | Cum verificăm |
|---|---|---|---|---|---|---|
| C1 | Doar adminii creează/modifică/șterg locații | Must | Securitate | Cod · echipa (analiza repo-ului) | R1 | Teste 401/403 |
| C2 | Un business poate gestiona doar promoțiile locației aprobate pentru el | Must | Securitate | Interviu localuri · de confirmat la interviu | R1 | Test: business A nu poate edita promoția lui B (403) |
| C3 | Un local cere revendicarea unei locații; adminul aprobă sau respinge | Must | Funcțional | Admini · de confirmat prin observație | Dovada că localul e al lor | Test pe flux + demo în pagina de admin |
| C4 | Userii văd doar promoțiile active (între `starts_at` și `ends_at`), pe hartă și în panoul locației | Must | Funcțional | Studenți, turiști · de confirmat la interviu / scenariu | O2 | Test cu promoție expirată / viitoare |
| C5 | Filtru „doar locații cu promoții” pe hartă | Should | Funcțional | Studenți · de confirmat la interviu | Găsești rapid ofertele | Test manual / e2e |

## 8. Primele trei architecture characteristics

| # | Architecture characteristic | Din ce cerință sau domain concern vine | Explicită / implicită |
|---|---|---|---|
| A1 | Securitate (autorizare pe roluri și pe proprietar) | C1, C2, C3 | Explicită |
| A2 | Integritatea datelor (promoție legată de o locație, expirare corectă) | C4 | Implicită |
| A3 | Deployability | O3, CI/CD existent | Explicită |

## 9. Întrebări pentru atelier

- Ajunge aprobarea de către admin ca dovadă că un local e al cuiva, sau ne trebuie altă verificare?
- Contează ca stakeholder confirmat un singur local intervievat?
- Ce hosting gratuit recomandați pentru FastAPI + Postgres?
- Rolurile le ținem într-o coloană `role` sau într-un tabel separat?
