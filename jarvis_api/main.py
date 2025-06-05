from fastapi import FastAPI, Request, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
API_KEY = os.getenv("API_KEY")
TABLE_NAME = "memory_fragments"

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

    try:
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
        print(f"📨 Supabase応答コード: {response.status_code}")
        print(f"📨 Supabase応答ボディ: {response.text}")
    except Exception as e:
        print(f"🔥 Supabase送信中にエラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Supabase POST失敗: {str(e)}")

    try:
        result_json = response.json()
    except Exception as e:
        result_json = {"error": f"レスポンスJSON化失敗: {str(e)}"}

    return {
        "status": response.status_code,
        "result": result_json
    }
