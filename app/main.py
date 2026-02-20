from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .config import settings
from .db import Base, engine, get_db
from . import models
from .security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from .openai_client import chat

app = FastAPI(title="Command Center API", version="1.0.0")

# CORS: okay for now; lock down origins later when you know your dashboard domain(s).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Database bootstrap ----
Base.metadata.create_all(bind=engine)

def ensure_admin(db: Session) -> None:
    # Create an admin user if one doesn't exist.
    if not settings.admin_email or not settings.admin_password:
        return
    existing = db.query(models.User).filter(models.User.email == settings.admin_email).first()
    if not existing:
        u = models.User(
            email=settings.admin_email,
            password_hash=hash_password(settings.admin_password),
            is_admin=True,
        )
        db.add(u)
        db.commit()

@app.on_event("startup")
def startup() -> None:
    db = Session(bind=engine)
    try:
        ensure_admin(db)
    finally:
        db.close()

# ---- API ----
@app.get("/api/ping")
def ping():
    return {"ok": True, "t": datetime.utcnow().isoformat() + "Z"}

@app.post("/api/auth/login")
def login(payload: dict, db: Session = Depends(get_db)):
    email = (payload or {}).get("email")
    password = (payload or {}).get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="email and password required")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/assistant")
async def assistant(body: dict, user=Depends(get_current_user)):
    prompt = (body or {}).get("prompt", "")
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="prompt required")
    return {"text": await chat(prompt)}

# ---- UI (optional) ----
WEB_DIR = Path(__file__).resolve().parent / "web"

if (WEB_DIR / "static").exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")

@app.get("/", include_in_schema=False)
def root():
    # If a UI is bundled, serve it. Otherwise, bounce to /docs.
    index = WEB_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return RedirectResponse(url="/docs")
