# AGENTS.md — ResourceNav

## Quick start
```bash
cd backend && cp .env.example .env   # edit DB creds
mycli -h 127.0.0.1 -uroot -proot123456 -e "SOURCE ../sql/init.sql" 2>/dev/null   # schema + seed data
uv sync                               # or: pip install -r requirements.txt
python main.py                        # uvicorn hot-reload on :8000
```

## Test MySQL container
- Containerized MySQL service, connect via `mycli -h 127.0.0.1 -uroot -proot123456`
- Set `.env`: `MYSQL_HOST=127.0.0.1 MYSQL_USER=root MYSQL_PASSWORD=root123456 MYSQL_DATABASE=resource_nav`

## Required SQL files

### Fresh init (run in order)
| File | Tables created |
|------|---------------|
| `sql/init.sql` | 12 张表: categories, organizations, owners, dev_machines, db_instances, resources, users, credentials, api_keys, api_key_logs, enum_items, nodes + 全部示例数据 |
| `sql/schema.sql` | 仅表结构（供查阅，init.sql 已包含） |
| `sql/seed.sql` | 仅示例数据（供查阅，init.sql 已包含） |

### Upgrade existing DB
| File | When needed |
|------|------------|
| `sql/status_migration.sql` | 旧版 TINYINT status → VARCHAR(20) 转换 |
| `sql/sample_resources_migration.sql` | 补充 测试/运维 分类的示例资源 |

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
- `frontend/` — 5 Vanilla HTML pages + shared `js/api.js`, served at `/frontend/`
- `sql/` — `init.sql` + migration files (apply manually when models change)
- `docs/` — API.md, FEATURES.md, DEPLOYMENT.md, CHANGELOG.md (most current)

## Key backend facts
- Auth: JWT (7d expiry) **or** API Key (bcrypt-hashed Bearer tokens)
- Guest user (id=0, role=guest) auto-returned when no token provided
- Permission functions in `resources.py`: `can_read()` / `can_manage()` — role + category based
- `routers/resources.py` is a catch-all: dev_machines, db_instances, resources, orgs, owners
- `routers/nodes.py` — CMDB node CRUD with API Key auth, under `/api/v1/nodes`
- `routers/api_keys.py` — API Key lifecycle management
- `routers/enum_items.py` — dynamic enum/select-option system
- 5 roles: guest, registered (read-only), learning_mentor, ops_expert, admin
- Default admin: `admin` / `admin123` (seeded in `sql/init.sql`)

## Conventions
- Response bodies are JSON, `Detail` strings in Chinese (e.g. "用户未找到")
- No SQLAlchemy migrations — edit models + write SQL migration in `sql/`
- Frontend is served by backend during dev — just refresh browser on frontend edits
