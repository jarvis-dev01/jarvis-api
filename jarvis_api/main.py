from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime
from supabase import create_client, Client
import os

app = FastAPI()

# 環境変数からSupabase接続情報を取得
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
API_KEY = os.getenv("API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# メモの構造定義
class MemoryItem(BaseModel):
    content: str
    role: str = "user"
    tag: str = ""
    type: str = "メモ"
    created_at: datetime = datetime.now()

# ✅ 生存確認用ルート（Render維持のため）
@app.get("/")
def root():
    return {"status": "ok", "message": "JARVIS API is alive"}

# 記憶を保存するAPIエンドポイント
@app.post("/record-memory")
def record_memory(item: MemoryItem, api_key: str = Query(None)):
    if api_key != API_KEY:
        return {"error": "Invalid API Key"}

    response = supabase.table("memories").insert({
        "content": item.content,
        "role": item.role,
        "tag": item.tag,
        "type": item.type,
        "created_at": item.created_at.isoformat()
    }).execute()
    return {"status": "success", "data": response.data}
