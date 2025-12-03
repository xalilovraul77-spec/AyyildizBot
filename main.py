from pyrogram import Client, filters
import requests
import json

# ───────── TELEGRAM AYARLARI ─────────
API_ID = 34645663
API_HASH = "4071e357a9e24e1926bda31da41aaea3"
SESSION = "AyyildizTim"

# ───────── GEMINI API ─────────
GEMINI_KEY = "AIzaSyCht-Ki_WSnmFy18zFLsYl76m-sS2J0Zdo"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"

# ───────── BOT DAVRANIŞI ─────────
BOT_NAME = "Asistan"
STYLE = "samimi ve net"
TOPICS = "Telegram, teknoloji"

SYSTEM_PROMPT = f"Adın {BOT_NAME}. {STYLE} tarzında konuş. Uzmanlık alanın: {TOPICS}. Türkçe ve kısa cevap ver."

# ───────── CLIENT ─────────
app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)


# ───────── GEMINI İSTƏK ─────────
def ask_gemini(user_text: str) -> str:
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": SYSTEM_PROMPT}]},
            {"role": "user", "parts": [{"text": user_text}]}
        ]
    }

    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=60)

        if r.status_code != 200:
            return f"❌ Gemini Error {r.status_code}: {r.text}"

        j = r.json()

        # ✅ Format-safe cevap çıkar
        content = j["candidates"][0]["content"]

        if "parts" in content:
            return content["parts"][0]["text"]

        elif "text" in content:
            return content["text"]

        else:
            return "❌ Gemini boş cevap verdi"

    except Exception as e:
        return f"❌ Gemini Exception: {e}"


# ───────── SADECE DM ─────────
@app.on_message(filters.private & filters.incoming)
async def auto_reply(client, message):
    if not message.text:
        return

    reply = ask_gemini(message.text)
    await message.reply_text(reply)

    print(f"[OK] DM => {reply[:80]}")


# ───────── START ─────────
print("✅ Gemini DM Bot başladı!")
app.run()
