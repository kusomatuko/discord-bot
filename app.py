import json
import urllib.request
from datetime import datetime, timedelta, timezone
from flask import Flask, request

app = Flask(__name__)

# DiscordのWebhook URL
DISCORD_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/1539471302715510874/--KVUupUWfcZsuPN4SlLXh5u0dITZ6Kv8jMTRB__LRpYvgjqgVjqbgopukhy4VS6Jsdz"
)


@app.route("/")
def index():
  # 1. 日本時間（JST）の現在日時を取得
  JST = timezone(timedelta(hours=+9), "JST")
  now = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")

  # 2. サイトにアクセスした相手のIPアドレスを抜き出す
  xff = request.headers.get("X-Forwarded-For")
  if xff:
    client_ip = xff.split(",")[0].strip()
  else:
    client_ip = request.remote_addr

  # 3. デバイス情報を取得
  user_agent = request.headers.get("User-Agent", "不明")

  # 4. どこから飛んできたか（リファラー）を取得
  referrer = request.headers.get("Referer", "直接アクセス（または不明）")

  # 5. IPアドレスからだいたいの位置情報（国・都市など）を調べる
  location_info = "不明"
  if client_ip and client_ip not in ["127.0.0.1", "localhost"]:
    try:
      url = f"http://ip-api.com/json/{client_ip}?lang=ja"
      req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
      with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        if data.get("status") == "success":
          country = data.get("country", "")
          region = data.get("regionName", "")
          city = data.get("city", "")
          location_info = f"{country} {region} {city}".strip()
    except Exception as e:
      print(f"位置情報取得エラー: {e}")

  # 6. Discordに送るメッセージを作成
  payload = {
      "content": (
          f"📥 **新しいアクセスがありました**\n"
          f"• **アクセス日時:** `{now}`\n"
          f"• **IPアドレス:** `{client_ip}`\n"
          f"• **推定地域:** `{location_info}`\n"
          f"• **流入元 (どこから):** `{referrer}`\n"
          f"• **デバイス情報:** `{user_agent}`"
      )
  }

  # 7. Discordへ送信
  try:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    urllib.request.urlopen(req)
  except Exception as e:
    print(f"Discord送信エラー: {e}")

  return "アクセスありがとうございます！"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
