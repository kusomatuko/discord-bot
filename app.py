import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 教えてくれたDiscordのWebhook URL
DISCORD_WEBHOOK_URL = (
    "https://discord.com/api/webhooks/1539471302715510874/--KVUupUWfcZsuPN4SlLXh5u0dITZ6Kv8jMTRB__LRpYvgjqgVjqbgopukhy4VS6Jsdz"
)


@app.route("/")
def index():
  # 1. サイトにアクセスした人の一番最初のIPアドレスを綺麗に抜き出す
  xff = request.headers.get("X-Forwarded-For")
  if xff:
    client_ip = xff.split(",")[0].strip()
  else:
    client_ip = request.remote_addr

  # 2. アクセスした人の端末情報（機種やブラウザなど）を取得
  user_agent = request.headers.get("User-Agent", "不明")

  # 3. Discordに送るメッセージを作成
  log_message = {
      "content": (
          f"📥 **新しいアクセスがありました**\n"
          f"• **IPアドレス:** `{client_ip}`\n"
          f"• **デバイス情報:** `{user_agent}`"
      )
  }

  # 4. DiscordのWebhookに送信
  try:
    requests.post(DISCORD_WEBHOOK_URL, json=log_message)
  except Exception as e:
    print(f"Discord送信エラー: {e}")

  return "アクセスありがとうございます！"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)



