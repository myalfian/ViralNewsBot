# === zip_all_source.py ===
# Fungsi: Zip seluruh folder dan file untuk ViralNewsBot
import shutil
import os

BASE_DIR = "/mnt/data/ViralNewsBotFull"
ZIP_OUTPUT = "/mnt/data/ViralNewsBotFull.zip"

# Hapus zip sebelumnya jika ada
if os.path.exists(ZIP_OUTPUT):
    os.remove(ZIP_OUTPUT)

# Kompres folder ke ZIP
shutil.make_archive(BASE_DIR, 'zip', BASE_DIR)

print("✅ ZIP berhasil dibuat di:", ZIP_OUTPUT)
