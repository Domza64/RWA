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
uvicorn app.main:app --reload
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

---

## Korisne naredbe

```bash
# -- Baza --
docker compose up -d db          # Pokreni PostgreSQL
docker compose ps                # Status kontejnera
docker compose logs db           # Logovi baze
docker compose down              # Zaustavi sve
docker compose down -v           # Zaustavi + obriši podatke (reset)

# -- Backend --
uvicorn app.main:app --reload    # Dev server s auto-reloadom
pytest                           # Pokreni testove
ruff check .                     # Lint (provjera kvalitete koda)
black .                          # Format (automatsko formatiranje)

# -- Migracije --
alembic upgrade head             # Primijeni sve migracije
alembic downgrade -1             # Rollback zadnje migracije
alembic revision --autogenerate -m "opis"  # Nova migracija
python -m app.seed               # Seed podatke u bazu

# -- Git --
git log --oneline --decorate     # Kratki pregled povijesti
git diff <commit1>..<commit2>    # Usporedba dva commita
git show <commit>                # Detalji jednog commita
```
