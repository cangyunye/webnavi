# AGENTS.md — ResourceNav

## Quick start
```bash
cd backend && cp .env.example .env   # edit DB creds
mycli -h 127.0.0.1 -uroot -proot123456 -e "SOURCE ../sql/init.sql" 2>/dev/null   # create DB + seed data
uv sync                               # or: pip install -r requirements.txt
python main.py                        # uvicorn hot-reload on :8000
```

## Test MySQL container
- Containerized MySQL service, connect via `mycli -h 127.0.0.1 -uroot -proot123456`
- Set `.env`: `MYSQL_HOST=127.0.0.1 MYSQL_USER=root MYSQL_PASSWORD=root123456 MYSQL_DATABASE=resource_nav`
- All DB operations (init, migration, verification) use this connection info

## Dependencies
- Two manifests: `requirements.txt` (pip) **and** `pyproject.toml` + `uv.lock` (uv). Prefer `uv sync`.
- `.python-version` = 3.14
- Aliyun PyPI mirror configured in `uv.lock`

## No QA infra
- **No tests** — any test framework, any test file. Don't try to run them.
- **No linter, no type checker, no formatter** configured.
- **No CI** — no `.github/` directory.

## Project structure
- `backend/` — FastAPI, entry: `main.py` → uvicorn `--reload` on port 8000
- `frontend/` — Vanilla HTML/CSS/JS, served by FastAPI at `/frontend/`, `/` → `/frontend/index.html`
- `sql/` — `init.sql` + migration files (apply manually when models change)
- `docs/` — API.md, FEATURES.md, DEPLOYMENT.md, CHANGELOG.md (more current than README for API details)

## Key backend facts
- Auth: JWT (7d expiry) **or** API Key (bcrypt-hashed Bearer tokens)
- Guest user (id=0, role=guest) auto-returned when no token provided
- `routers/resources.py` is a catch-all: dev_machines, db_instances, resources, organizations, owners
- `routers/nodes.py` — CMDB-style node CRUD with API Key auth, under `/api/v1/nodes`
- `routers/api_keys.py` — API Key lifecycle management
- `routers/enum_items.py` — dynamic enum/select-option system
- Permission check in `deps.py` line 198: guest-accessible categories = ["学习", "AI", "软件资源", "测试"]
- Default admin: `admin` / `admin123` (seeded in `sql/init.sql`)
- `check_category_permission` in `resources.py` line 23 — separate from `deps.py` check; both exist

## Conventions
- Response bodies are JSON, `Detail` strings in Chinese (e.g. "用户未找到")
- No SQLAlchemy migrations — edit models + write SQL migration in `sql/`
- Frontend is served by backend during dev — just refresh browser on frontend edits
