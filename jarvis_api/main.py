from fastapi import FastAPI, Request, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
API_KEY = os.getenv("API_KEY")  # ← 追加
TABLE_NAME = "memory_fragments"

@app.post("/record-memory")
async def record_memory(request: Request):
    client_key = request.headers.get("apikey")

    # ✅ API用の鍵と比較するよう修正
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

    data = await request.json()

    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}",
        json=data,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    )

    return {
        "status": response.status_code,
        "result": response.json()
    }
