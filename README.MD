# Unit Logbook — REST API

Backend admission task (`01b-swdev-backend-api`) for the ICT Conscript Program.

A small REST API that stores a platoon's field log entries in SQLite and serves
them as JSON, so other apps (like the frontend task) can read and add entries.

## Live URL

https://test-ictconscript-admission-250p.onrender.com

Check it: [`/health`](https://test-ictconscript-admission-250p.onrender.com/health)
· [`/entries`](https://test-ictconscript-admission-250p.onrender.com/entries)

Runs on Render's free tier, which sleeps after ~15 min idle. First request after
that takes 30–60s to wake up, then it's fast.

There's also a small browser test console at `/static/index.html` for adding/viewing
entries by hand. It's just a testing aid, not part of the API.

## Stack

- Python 3.12 + Flask
- SQLite (`sqlite3` from the standard library)
- gunicorn as the server
- Docker, deployed on Render

### Why Flask and not FastAPI

I built this on an Android phone in Termux during service, since I didn't have a
computer for most of it. FastAPI needs pydantic-core, which is compiled from Rust
and has no prebuilt package for Android/aarch64, so it won't install there. Flask
is pure Python and installs fine, and the task lists it as an allowed option. The
tradeoff is that I write the input validation by hand instead of letting Pydantic
do it — that's in `main.py`.

## Routes

Everything returns JSON except `/health` (plain `OK`). Bad input returns a 4xx and
a JSON error like `{"error": "..."}`.

| Method | Path | What it does | OK | Error |
|--------|------|--------------|-----|-------|
| GET | `/health` | health check | `200` `OK` | — |
| GET | `/entries` | all entries, newest first | `200` | — |
| GET | `/entries/<id>` | one entry by id | `200` | `404` if not found |
| POST | `/entries` | add an entry | `201` | `400` on bad input |

An entry looks like this:

```json
{
  "id": 1,
  "title": "Night perimeter check",
  "body": "All clear around main gate.",
  "isoTime": "2025-05-14T21:30:00Z",
  "lat": 60.1503,
  "lon": 25.0293
}
```

`lat`/`lon` are null if there's no position.

### POST /entries

Send:

```json
{
  "title": "Patrol departure",
  "body": "Alpha team left camp.",
  "lat": 60.15,
  "lon": 25.04
}
```

`title` is required (string, max 120), `body` is required (string), `lat`/`lon` are
optional numbers. The server sets `id` and `isoTime` itself (client doesn't send
them — that way entries can't be backdated). Returns the created entry with `201`.

Validation, each returns `400`:
- title missing / not a string / over 120 chars
- body missing / not a string
- lat or lon present but not a number
- body isn't valid JSON

### Examples

```bash
curl https://test-ictconscript-admission-250p.onrender.com/entries

curl https://test-ictconscript-admission-250p.onrender.com/entries/3

curl -X POST https://test-ictconscript-admission-250p.onrender.com/entries \
  -H "Content-Type: application/json" \
  -d '{"title": "Drone sighting", "body": "Quad-copter to the north", "lat": 60.157, "lon": 25.047}'
```

## Files

```
main.py       routes, validation, JSON responses
database.py   SQLite: connection, table, queries
seed.py       loads the 10 sample entries from data.json
data.json     sample entries
static/       browser test console
Dockerfile    container build
```

A few notes:
- SQL is kept in `database.py`, out of `main.py`. Queries use `?` placeholders so
  user input can't be injected into the SQL.
- Sorting newest-first is done in the query (`ORDER BY isoTime DESC`), not in Python.
- The database gets created and seeded during the Docker build, so the container
  already has the 10 entries when it starts.

## Running it

Python:

```bash
pip install flask gunicorn
python -c "from database import init_db; init_db()"
python seed.py
python main.py
```

Docker:

```bash
docker build -t logbook .
docker run -p 8000:8000 logbook
```

## Note on persistence

SQLite survives a normal process restart. But the free hosting has an ephemeral
filesystem, so if the container restarts, the database resets to the seeded sample
data — entries added at runtime don't survive a redeploy. For real use this would
need a mounted volume or a managed database, but the task asked for SQLite so I
left it there.

## Where this was built

Written and tested on an Android phone (Termux) during service, then containerized
and deployed. Docker build and the local container run were checked on a PC.
