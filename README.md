# Command Center (Render-Ready) — Drop-in Deploy

This ZIP is a **single-service Render Web Service** project (FastAPI).
Upload to GitHub OR deploy on Render from GitHub.

## What this is
- FastAPI backend ("brain")
- JWT auth (required)
- SQLite by default (works on Render, but may reset on redeploy unless you add a disk or Postgres)
- Optional OpenAI endpoint (enabled when `OPENAI_API_KEY` is set)

---

## Fastest deploy (GitHub → Render)

### A) GitHub (no git required)
1. Create a GitHub repo (any name).
2. Click **Add file → Upload files**.
3. Upload **everything inside this ZIP** (drag the folder contents into GitHub).
4. Click **Commit changes**.

### B) Render
1. Render → **New +** → **Web Service**
2. **Connect GitHub** → pick your repo
3. Environment: **Docker**
4. Plan: Free (ok for testing)

Render will auto-detect `Dockerfile`. No build/start commands needed.

### C) REQUIRED Environment Variables (Render → Environment)
Set these keys:

- `JWT_SECRET` = 8sJ2hPx596CQzkR8eh8Q6w4xTL5dgIWhIt1K50g1xmBIJdoK
- `ADMIN_EMAIL` = your email
- `ADMIN_PASSWORD` = a strong password

Optional:
- `OPENAI_API_KEY` = your OpenAI key
- `OPENAI_MODEL` = gpt-4o-mini

Click **Save Changes** → Render redeploys.

### D) Verify
Open:
`https://<your-service>.onrender.com/api/ping`

Expected:
`{"ok": true, "t": "..."}`

---

## Persistence (important)
SQLite file lives in the container filesystem. On free tier, redeploys can wipe it.
For real persistence choose ONE:
- Add a **Render Disk** and set `DATABASE_URL=sqlite:////var/data/command_center.db`
- OR add **Render Postgres** and set `DATABASE_URL` to the Postgres connection string

Build: 2026-02-20
