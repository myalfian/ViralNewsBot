# === CapCut & FFmpeg + Flask Dashboard ===
# Struktur: /automation/capcut_ffmpeg.py dan /dashboard/app.py

# ---------- capcut_ffmpeg.py ----------
# Fungsi: generate video otomatis dari script berita & gambar
import os
import subprocess
from moviepy.editor import concatenate_videoclips, TextClip, CompositeVideoClip, ImageClip

def create_video_from_news(news_items, output_path="output_news_video.mp4"):
    clips = []
    for news in news_items:
        img = ImageClip(news['image']).set_duration(5).resize(width=1080)
        text = TextClip(news['title'], fontsize=48, color='white', size=(1000, None), method='caption')
        text = text.set_position(('center', 'bottom')).set_duration(5)
        final = CompositeVideoClip([img, text])
        clips.append(final)
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(output_path, fps=24)

# Example usage:
# create_video_from_news([
#     {'title': 'Berita Viral 1', 'image': 'screenshots/berita1.png'},
#     {'title': 'Berita Viral 2', 'image': 'screenshots/berita2.png'},
# ])

# ---------- Flask Dashboard (app.py) ----------
from flask import Flask, request, render_template, send_file
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    news_data = json.loads(request.form['news'])
    output_path = "static/output_video.mp4"
    from automation.capcut_ffmpeg import create_video_from_news
    create_video_from_news(news_data, output_path)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

# ---------- templates/index.html ----------
# Simpel form HTML:
# <form method="POST" action="/generate">
#   <textarea name="news" rows="10" cols="50">[{"title": "Judul 1", "image": "screenshots/berita1.png"}]</textarea>
#   <br><button type="submit">Generate Video</button>
# </form>

# ---------- Kebutuhan folder ----------
# /automation/capcut_ffmpeg.py
# /dashboard/app.py
# /dashboard/templates/index.html
# /screenshots/beritaX.png
# /static/output_video.mp4 (output)

# Untuk menjalankan:
# $ cd dashboard
# $ flask run

# Untuk FFmpeg CLI-style (opsional):
# subprocess.run(["ffmpeg", "-loop", "1", "-i", img, "-t", "5", "-vf", "drawtext=fontfile=Arial.ttf:text='...'"])
