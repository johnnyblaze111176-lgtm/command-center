import httpx
from .config import settings

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

async def chat(prompt: str) -> str:
    if not settings.openai_api_key:
        return "OPENAI_API_KEY not set on server. Add it to enable GPT."
    headers = {"Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role":"system","content":"You are an efficient command center assistant. Be concise and actionable."},
            {"role":"user","content": prompt},
        ],
        "temperature": 0.4
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(OPENAI_URL, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        return (data.get("choices",[{}])[0].get("message",{}).get("content") or "").strip()
