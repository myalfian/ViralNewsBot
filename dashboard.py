# === dashboard.py ===
# Web UI sederhana pakai Flask
from flask import Flask, jsonify, render_template_string
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open("viral_script_1.txt", encoding="utf-8") as f:
        script = f.read()
    return render_template_string("""
    <h1>📰 Viral News Dashboard</h1>
    <pre>{{script}}</pre>
    """, script=script)

@app.route('/api/news')
def api_news():
    with open("viral_script_1.txt", encoding="utf-8") as f:
        script = f.read()
    return jsonify({"script": script})

if __name__ == '__main__':
    app.run(debug=True)