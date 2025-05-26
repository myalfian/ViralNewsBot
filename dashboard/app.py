# === ViralNewsBot ===
# Tujuan: Mengotomatiskan pengumpulan, analisis, dan pembuatan script berita viral mingguan
# Tools: Python, Supabase, ElevenLabs, GitHub CI/CD, ChatGPT, CapCut, Canva, Flask

# === 1. Scraper Berita dari Media Mainstream ===
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import feedparser
import json
import re
import os
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Daftar RSS feed atau halaman utama yang dapat digunakan
RSS_FEEDS = {
    "Kompas": "https://www.kompas.com/feed",
    "Antaranews": "https://www.antaranews.com/rss/nasional.xml",
    "CNN Indonesia": "https://www.cnnindonesia.com/nasional/rss",
    "Detik": "https://rss.detik.com/index.php/detiknews",
    "Tempo": "https://rss.tempo.co/nasional"
}

# Ambil artikel terbaru dan simpan
def fetch_rss_articles():
    articles = []
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            articles.append({
                "source": source,
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", ""),
                "published": entry.get("published", "")
            })
    return articles

# === 2. Analisis Viralitas ===
VIRAL_KEYWORDS = ["viral", "trending", "heboh", "ramai", "gempar", "kontroversi", "netizen"]

def calculate_virality_score(article):
    title = article['title'].lower()
    summary = article['summary'].lower()
    score = sum(1 for word in VIRAL_KEYWORDS if word in title or word in summary)
    article['virality_score'] = score
    return article

# === 3. Script Generator ===
def generate_video_script(article, index):
    title = article['title']
    link = article['link']
    virality_score = article['virality_score']
    
    hook = f"Wah, netizen rame banget bahas ini minggu ini!"
    main_content = f"Berita dari {article['source']} ini bikin heboh netizen. {article['summary'][:240]}..."
    conclusion = "Gimana menurut kalian? Comment di bawah ya!"

    script = f"""
VIDEO BERITA VIRAL MINGGU KE-{index}
[{title}]

[HOOK - 10-15 detik]
{hook}

[MAIN CONTENT - 40-50 detik]
{main_content}

[CONCLUSION - 10-15 detik]
{conclusion}

Source: {link}
Virality Score: {virality_score}
"""
    return script

# === 4. Screenshot Gambar Berita ===
def capture_screenshot(link, index):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 720)
    driver.get(link)
    screenshot_path = f"screenshots/screen_{index}.png"
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path

# === 5. Supabase Integration ===
from supabase import create_client, Client

SUPABASE_URL = "https://sbbqgikkjzodxgcgljht.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNiYnFnaWtranpvZHhnY2dsamh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgyNDA2OTUsImV4cCI6MjA2MzgxNjY5NX0.lYvlicnxzhg3LWwqYn5jontBbzZG-jdM1EyGL5MrrHA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_to_supabase(article):
    data = {
        "title": article["title"],
        "link": article["link"],
        "summary": article["summary"],
        "source": article["source"],
        "virality_score": article["virality_score"]
    }
    supabase.table("viral_news").insert(data).execute()

# === 6. Video Template Automation (FFmpeg) ===
def generate_video_ffmpeg(script_path, image_path, index):
    output_video = f"videos/video_{index}.mp4"
    os.makedirs("videos", exist_ok=True)
    cmd = f"ffmpeg -loop 1 -i {image_path} -vf scale=720:1280 -c:v libx264 -t 60 -pix_fmt yuv420p -y {output_video}"
    os.system(cmd)
    return output_video

# === 7. Dashboard Flask ===
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    data = supabase.table("viral_news").select("*").execute()
    return jsonify(data.data)

# === 8. Main Orkestrasi ===
def main():
    articles = fetch_rss_articles()
    articles = [calculate_virality_score(a) for a in articles]
    viral_articles = sorted(articles, key=lambda x: x['virality_score'], reverse=True)[:7]

    for idx, article in enumerate(viral_articles, start=1):
        script = generate_video_script(article, idx)
        save_to_supabase(article)
        with open(f"viral_script_{idx}.txt", "w", encoding="utf-8") as f:
            f.write(script)
        screenshot_path = capture_screenshot(article['link'], idx)
        generate_video_ffmpeg(f"viral_script_{idx}.txt", screenshot_path, idx)
        print(script)

if __name__ == "__main__":
    main()
    app.run(debug=True)
