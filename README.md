# DevOps Project — Task List

Application simple (frontend React + backend FastAPI) utilisée tout au long du cursus DevOps.

> En entreprise, le frontend et le backend sont généralement dans des dépôts (repos) séparés, avec chacun son propre pipeline CI/CD. Ici, on les met dans le même repo pour simplifier l'apprentissage.

## Architecture

```
┌──────────────┐     HTTP      ┌───────────────────┐     SQL       ┌──────────────┐
│              │   /api/...    │                   │               │              │
│   Frontend   │──────────────▶│     Backend       │──────────────▶│  PostgreSQL   │
│  (React +    │               │   (FastAPI +      │               │  (données)   │
│   nginx)     │◀──────────────│    Python)        │◀──────────────│              │
│              │     JSON      │                   │    rows       │              │
│   port 80    │               │    port 8000      │               │   port 5432  │
└──────────────┘               └───────────────────┘               └──────────────┘
       │                              │                                   │
       └──────────────────────────────┴───────────────────────────────────┘
                            Docker Compose (un réseau commun)
```

- Le **frontend** est une page web (React) servie par **nginx**. L'utilisateur voit la liste des tâches.
- **nginx** fait office de **reverse proxy** : les requêtes `/api` sont redirigées vers le backend.
- Le **backend** est une API Python (FastAPI). Il gère les tâches (créer, lister, toggler, supprimer).
- **PostgreSQL** stocke les données. Sans Docker (`DATABASE_URL` absente), le backend utilise une liste en mémoire.

## Structure

```
.github/workflows/
  ci.yml              → Pipeline CI/CD (lint → test → build → push)
frontend/             → Vite + React (géré par Bun)
  Dockerfile          → Multi-stage build (Bun → nginx)
  nginx.conf          → Reverse proxy vers le backend
backend/              → Python FastAPI (géré par uv)
  Dockerfile          → Image Python avec uv
docker-compose.yml    → Backend + Frontend + PostgreSQL
```

## Lancer en local (sans Docker)

**Backend :**
```bash
cd backend
uv sync
uv run uvicorn main:app --reload
# L'API tourne sur http://localhost:8000
# Sans DATABASE_URL → stockage in-memory (pas besoin de PostgreSQL)
```

**Frontend :**
```bash
cd frontend
bun install
bun run dev
# Le frontend tourne sur http://localhost:3000
# Les appels /api sont proxyfiés vers le backend
```

## Lancer avec Docker Compose

```bash
docker compose up -d --build
# Frontend : http://localhost (port 80)
# Backend :  http://localhost:8000
# PostgreSQL : port 5432 (accessible uniquement depuis le backend)
```

## API Endpoints

| Méthode | URL | Description |
|---------|-----|-------------|
| `GET` | `/api/tasks` | Lister les tâches |
| `POST` | `/api/tasks` | Créer une tâche (`{"title": "..."}`) |
| `PATCH` | `/api/tasks/{id}` | Toggler done/not done |
| `DELETE` | `/api/tasks/{id}` | Supprimer une tâche |
| `GET` | `/api/health` | Health check |

## Linting

```bash
# Backend (Ruff)
cd backend && uv run ruff check .

# Frontend (Oxlint)
cd frontend && bunx oxlint .
```

## Tests

```bash
cd backend && uv run pytest
# 7 tests : GET, POST, PATCH, PATCH 404, DELETE, DELETE 404, health
```
