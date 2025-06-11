from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse
import requests
import os
from dotenv import load_dotenv
import json

# ✅ .env のパスを明示指定
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
API_KEY = os.getenv("API_KEY")
TABLE_NAME = "memory_fragments"

print(f"🧪 環境変数 SUPABASE_KEY = {SUPABASE_KEY}")

app = FastAPI()

# 🔐 POST: 記憶を保存
@app.post("/record-memory")
async def record_memory(request: Request):
    client_key = request.headers.get("apikey")
    print(f"🔑 client_key = {client_key}")

    if client_key != API_KEY:
        print("❌ APIキーが一致しません")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

    try:
        data = await request.json()
        print(f"📦 受信データ = {data}")
    except Exception as e:
        print(f"⚠️ JSON読み込みエラー: {str(e)}")
        raise HTTPException(status_code=400, detail=f"JSON読み込み失敗: {str(e)}")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    response = requests.post(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}", headers=headers, json=data)
    print(f"📤 Supabase応答 = {response.text}")

    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Supabaseへの保存に失敗しました")

    return {"status": "ok", "data": response.json()}


# 📥 GET: 記憶を取得（軽量バージョン）
@app.get("/get-memory")
def get_memory(tag: str = Query(None)):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    # 🔽 必要カラムだけ選択＋最大10件に制限
    base_url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?select=content,created_at&limit=10"

    if tag:
        url = f"{base_url}&tag=eq.{tag}"
    else:
        url = base_url

    response = requests.get(url, headers=headers)
    print(f"📤 Supabaseからの応答: {response.text}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Supabaseからの取得に失敗しました")

    return response.json()
