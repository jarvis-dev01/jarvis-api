from fastapi import FastAPI, Request, HTTPException
import requests
import os
from dotenv import load_dotenv

# .envファイルの読み込み（SUPABASE情報が入っている）
load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "memory_fragments"

@app.post("/record-memory")
async def record_memory(request: Request):
    # 🔐 クライアントから送られてきた「鍵（APIキー）」を取り出す
    client_key = request.headers.get("apikey")

    # 🔍 鍵が正しいかチェック（間違ってたら403エラー）
    if client_key != SUPABASE_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

    # ✅ 正しければ、記憶データを読み取ってSupabaseに保存
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
