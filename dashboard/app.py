from flask import Flask, render_template, jsonify
from auth import require_auth
from collectors import snapshot

app = Flask(__name__)

@app.route("/")
@require_auth
def index():
    return render_template("index.html")

@app.route("/api/status")
@require_auth
def api_status():
    return jsonify(snapshot())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
