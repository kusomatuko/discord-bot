from flask import Flask, request
import urllib.request
import json

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = "あなたのDiscordのWebhook URL"
    data = {"content": f"IPアドレス: {ip}"}
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        urllib.request.urlopen(req)
    except:
        pass
    return "ok"

if __name__ == '__main__':
    app.run()
