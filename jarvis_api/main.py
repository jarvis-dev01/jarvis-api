from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
import os
import requests

app = FastAPI()

# 環境変数からAPIキーを読み込む
API_KEY = os.getenv("API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# モデル定義
class MemoryItem(BaseModel):
    content: str
    role: str = "system"
    tag: str = ""
    type: str = "log"

# POSTエンドポイント：記憶を保存（認証はクエリパラメータで受け取る）
@app.post("/record-memory")
async def record_memory(item: MemoryItem, api_key: str = Query(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

    now = datetime.utcnow().isoformat()
    payload = {
        "content": item.content,
        "role": item.role,
        "tag": item.tag,
        "type": item.type,
        "created_at": now
    }
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{SUPABASE_URL}/rest/v1/memory_fragments", json=payload, headers=headers)

    if response.status_code != 201:
        raise HTTPException(status_code=500, detail=f"Supabase Error: {response.text}")
    
    return {"status": "success", "supabase_response": response.json()}

# GETエンドポイント：記憶を取得（仮実装）
@app.get("/get-memory")
async def get_memory(limit: int = 10):
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }
    response = requests.get(f"{SUPABASE_URL}/rest/v1/memory_fragments?limit={limit}&order=created_at.desc", headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Supabase GET failed")

    return response.json()
