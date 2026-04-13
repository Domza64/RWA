# Jira 2

Sustav za pračenje zadataka u timu.
Projekt za kolegij **Razvoj web aplikacija** — SIT UNIZD.

---

## Tehnologije

| Sloj    | Stack                                 |
| ------- | ------------------------------------- |
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.0 |
| Baza    | PostgreSQL 16 (Docker Compose)        |
| Auth    | JWT (access + refresh tokeni)         |

---

## Preduvjeti

Prije pokretanja projekta trebate imati instalirano:

- **Python** ≥ 3.11 — [python.org/downloads](https://www.python.org/downloads/)
- **Docker Desktop** — [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
- **Git** — [git-scm.com](https://git-scm.com/)

---

## Brzo pokretanje

### 1. Setup

```bash
git clone <url>
cd <repo>

# env
cp .env.example .env        # Linux/macOS
Copy-Item .env.example .env # Windows
```

### 2. Dev servisi

```bash
docker compose -f dev-compose.yml up -d
```

### 3. Backend

```bash
cd api

python -m venv .venv
# activate:
# Linux/macOS: source .venv/bin/activate
# Windows:     .venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn app.main:app --reload  # run app
pytest # run tests
```

### 4. Servisi

- [http://127.0.0.1:8000](http://127.0.0.1:8000) - API
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - Swagger
- [http://127.0.0.1:9090](http://127.0.0.1:9090) - PG Web

---

## Git konvencije

### Commit poruke

Format: `<tip>(<scope>): <opis>`

| Tip        | Značenje                             |
|------------|--------------------------------------|
| `feat`     | Nova funkcionalnost                  |
| `fix`      | Ispravka buga                        |
| `refactor` | Promjena bez nove funkcionalnosti    |
| `chore`    | Tooling, config, infrastruktura      |
| `docs`     | Dokumentacija                        |
| `test`     | Testovi                              |

## Migracije Baze (Alembic)

Alembic je "version control za bazu" — svaka promjena modela zahtijeva novu migraciju.

```bash
cd api

# Primijeni sve migracije (kreira tablice):
alembic upgrade head

# Rollback zadnje migracije:
alembic downgrade -1

# Generiraj novu migraciju nakon promjene modela:
alembic revision --autogenerate -m "opis promjene"

# Prikaži povijest migracija:
alembic history
```
## TODOs

## Auth

- [x] `POST /auth/register` → register
- [x] `POST /auth/login` → login, get JWT and refresh token
- [x] `GET /auth/me` → get current user data

---
## Health

- [x] `GET /health`

---
## Board

- [x] `GET /boards` → list of boards for current user
- [x] `POST /boards` → create new board
- [ ] `DELETE /boards/{board_id}` → delete board
- [ ] `PUT /boards/{board_id}` → edit title/desc
- [x] `GET /boards/{board_id}/members` → get members of the board (**paginated route...**)
- [x] `POST /boards/{board_id}/members` → add member to the board
- [ ] `DELETE /boards/{board_id}/members/{member_id}` → remove member from the board
- [ ] `PUT /boards/{board_id}/members/{member_id}` → update board member
- [x] `GET /boards/{board_id}/workflow-stages → get all ticket status for board
- [x] `POST /boards/{board_id}/workflow-stage` → create ticket status
- [ ] `DELETE /boards/{board_id}/workflow-stages/{id}` → delete ticket status
- [ ] `PUT /boards/{board_id}/workflow-stages/{id}` → update ticket status
- [x] `POST /boards/{board_id}/ticket` → create ticket

> **Ticket status** -> vertical columns with text like, todo, in progress, done... that display actual tickets

---
## Ticket

- [x] `GET /ticket/{ticket_id}` → get ticket
- [ ] `PUT /ticket/{ticket_id}` → update ticket
- [ ] `DELETE /ticket/{ticket_id}` → delete ticket
- [ ] `GET /ticket/assigned` → List of assigned tickets
- [ ] `GET /ticket/reported` → List of reported tickets

---
## Misc

- [ ] Endpoint za reorder workflow stages
- [ ] Endpoint za reorder tickets
