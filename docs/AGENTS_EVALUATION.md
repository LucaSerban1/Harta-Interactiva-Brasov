# Evaluation of the AI Agents Used During Development

This document evaluates the AI agents used while developing this project: what tasks they were given, how they performed, where human intervention was needed, and what conclusions we drew.

## Agents used

| Agent | Model(s) | Role in the project |
|-------|----------|----------------|
| **Claude Code** (CLI) | Claude Sonnet 4.6, Claude Fable 5 | Main agent: feature implementation, CI/CD, fixes, code review, documentation |
| **Claude Code subagents** (`Explore`) | Sonnet | Parallel bug hunting during code review (multi-angle analysis) |

## Tasks given to the agents and results

### 1. CI setup (GitHub Actions)

**Task:** a CI workflow with backend tests (pytest + PostgreSQL as a service container), frontend lint and build.

**Result:** the final workflow works, but it required **4 fix iterations** visible in the git history:

- `f4edfc5` — wrong `DATABASE_URL` for alembic + Node version too old (18 → 20)
- `33d9600` — broken imports in `seed.py`, eslint errors, unused variable
- `6c3e876` — unused `catch` variable (`no-unused-vars` rule)
- `aa9b143` — TypeScript type errors in `AIAssistant` and the `AIResponse` type

**Evaluation:** the agent quickly produced a correct skeleton but did not anticipate the differences between the local environment and the CI runner (versions, environment variables). The iterations were fast, however — each fix took minutes, guided by the CI logs.

### 2. CD pipeline (PR [#31](https://github.com/LucaSerban1/Harta-Interactiva-Brasov/pull/31))

**Task:** Dockerfiles for the backend and frontend + a workflow that automatically publishes the images to GitHub Container Registry.

**Result:** a working implementation on the first code iteration, but **the automated code review found 3 major problems** in the agent's own implementation (see the next section), which were then fixed in a follow-up commit (`1f615d7`).

**Evaluation:** a good example of "AI that writes + AI that verifies" — the first version was plausible and would have gone unnoticed on a superficial read, but it had real deployment gaps (migrations never run, no gating on CI).

### 3. Automated code review (PR #31)

**Task:** a high-recall review: 7 analysis angles run by parallel subagents → 12 bug candidates → individual verification → final findings posted as review comments on the PR.

**Result:**

| Metric | Value |
|---------|---------|
| Candidates found by the subagents | 12 |
| Confirmed/plausible findings | 5 (3 major, 2 minor) |
| False positives rejected during verification | 2 |
| Findings turned into issues | 1 ([#32](https://github.com/LucaSerban1/Harta-Interactiva-Brasov/issues/32)) |

Examples of real findings: CD published images even when tests failed; the backend container never ran the alembic migrations; the frontend bundle embeds a hardcoded API URL.

Examples of rejected false positives: one subagent claimed that `IMAGE_PREFIX` contained uppercase letters and GHCR would reject it — false, the value was already lowercase (a typical hallucination: the agent confused the repository name with the variable's value).

**Evaluation:** the **verification** step is essential — without it, ~17% of the findings would have been noise. With verification, the review found problems that the authors (human + AI) had missed.

### 4. Documentation and UML diagrams

**Task:** README, Mermaid diagrams (class, sequence, ER), AI documentation.

**Result:** mostly correct on the first attempt; the diagrams only needed small Mermaid syntax adjustments. The agent read the actual code (SQLAlchemy models, the auth router) before drawing the diagrams, so they reflect the real schema, not an invented one.

## Evaluation criteria and scores

| Criterion | Score (1–5) | Notes |
|----------|-----------|------------|
| **Correctness of generated code** | 4 | The code compiles and works locally almost every time; problems appear at the system's edges (CI, deployment, configuration) |
| **Autonomy** | 4 | Can carry a full issue → branch → PR → review → merge flow on its own; asks for confirmation on architectural decisions |
| **Speed** | 5 | Tasks that would take hours (a full CD pipeline + docs) finish in minutes |
| **Anticipating the production environment** | 3 | The weakest point: local vs. CI vs. container differences required iterations |
| **Code review quality** | 4 | Finds real bugs missed by humans, but also produces false positives — a verification step is required |
| **Documentation** | 5 | The generated documentation is grounded in the real code, not generic |

## Conclusions

1. **AI does not replace code review — it powers it.** The most valuable results came from combining a *writing agent* + a *verifying agent* + a *human who decides* — the automated review found real bugs in code that was itself written by AI.
2. **CI logs are the agent's best feedback.** All 4 CI fix iterations were resolved quickly because the agent received the exact error log.
3. **Human verification remains mandatory at the system's edges:** secrets, environment variables, registry permissions, production behaviour.
4. **False positives are manageable** as long as the workflow includes an explicit verification step for every finding before it is reported.
