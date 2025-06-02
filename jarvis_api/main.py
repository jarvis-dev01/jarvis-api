from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # .envファイルを読み込む

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "memory_fragments"

@app.post("/record-memory")
async def record_memory(request: Request):
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
    return {"status": response.status_code, "result": response.json()}
