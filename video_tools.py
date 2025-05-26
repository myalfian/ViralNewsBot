# === video_tools.py ===
# Fungsi: Generate screenshot berita + video otomatis pakai FFmpeg
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess

SCREENSHOT_DIR = "output/screenshots"
VIDEO_DIR = "output/videos"
SCRIPT_DIR = "output/scripts"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(SCRIPT_DIR, exist_ok=True)

def take_screenshot(url, output_path):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 720)
    driver.get(url)
    time.sleep(3)
    driver.save_screenshot(output_path)
    driver.quit()

def generate_video_from_image(image_path, audio_path, output_path):
    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_path,
        '-i', audio_path,
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        output_path
    ]
    subprocess.run(cmd)