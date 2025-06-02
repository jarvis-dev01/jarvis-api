import os
import requests
import re
from dotenv import load_dotenv

# .envの読み込み
load_dotenv()

# .envから環境変数取得（← SUPABASE_URL / SUPABASE_KEY に合わせて修正済）
SUPABASE_API_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_KEY")

def post_to_memory(content: str, type_: str = "raw") -> bool:
    """
    Supabaseに記憶データをPOST送信する（ログ付き）
    """
    url = f"{SUPABASE_API_URL}/rest/v1/memory_fragments"
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    data = {
        "content": content,
        "type": type_
    }

    # ✅ ログ出力：送信先・データ内容
    print(f"\n📡 POST送信中: {url}")
    print(f"📄 データ内容: {data}")

    response = requests.post(url, headers=headers, json=data)

    # ✅ 結果ログ
    if response.status_code == 201:
        print("✅ 記録成功: Supabaseに保存されました。")
        return True
    else:
        print(f"❌ 記録失敗: ステータスコード {response.status_code}")
        print("🔍 詳細:", response.text)
        return False

def judge_memory_intent(text: str) -> str | None:
    """
    トニー様の自然な発話パターンに対応した記録判定ロジック（v1.8）
    """
    custom_patterns = [
        r"記録しといて", r"記録して", r"記録しろ", r"記録に残せ",
        r"覚えておいて", r"覚えといて", r"覚えろ",
        r"記憶しといて", r"記憶して", r"記憶しろ",
        r"メモリしろ", r"メモリして", r"メモリに残せ",
        r"ログに残せ"
    ]

    pattern = re.compile("|".join(custom_patterns), re.IGNORECASE)
    if pattern.search(text):
        return text.strip()
    return None
