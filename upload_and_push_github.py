# === upload_and_push_github.py ===
# Fungsi: Ekstrak ZIP dan push otomatis ke GitHub
import os
import subprocess
import zipfile

ZIP_PATH = "/mnt/data/ViralNewsBot.zip"
EXTRACT_DIR = "/mnt/data/ViralNewsBotRepo"
REPO_URL = "https://github.com/myalfian/ViralNewsBot.git"

# 1. Ekstrak ZIP
os.makedirs(EXTRACT_DIR, exist_ok=True)
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

# 2. Git Init + Push
os.chdir(EXTRACT_DIR)

if not os.path.exists(".git"):
    subprocess.run(["git", "init"])
    subprocess.run(["git", "remote", "add", "origin", REPO_URL])

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Initial push: video tools, dashboard, script"])
subprocess.run(["git", "branch", "-M", "main"])
subprocess.run(["git", "push", "-u", "origin", "main"])
