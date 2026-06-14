"""
utils.py
Fungsi bantu umum: konversi gambar, format tanggal, path management.
"""

import os
from datetime import datetime
import numpy as np
import cv2


def ensure_dirs():
    """Pastikan folder output tersedia."""
    os.makedirs("outputs/reports", exist_ok=True)
    os.makedirs("outputs/images", exist_ok=True)
    os.makedirs("data", exist_ok=True)


def timestamp_now() -> str:
    """Format timestamp untuk nama file & histori."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def readable_timestamp() -> str:
    """Format timestamp ramah-baca untuk dashboard."""
    return datetime.now().strftime("%d %B %Y, %H:%M:%S")


def pil_to_cv2(pil_image):
    """Konversi PIL Image (RGB) ke array OpenCV (BGR)."""
    arr = np.array(pil_image.convert("RGB"))
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def cv2_to_rgb(cv2_image):
    """Konversi array OpenCV (BGR) ke RGB untuk ditampilkan di Streamlit."""
    return cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)


def save_image(cv2_image, filename: str) -> str:
    """Simpan gambar hasil proses ke outputs/images/ dan kembalikan path."""
    ensure_dirs()
    path = os.path.join("outputs", "images", filename)
    cv2.imwrite(path, cv2_image)
    return path


def safe_filename(name: str) -> str:
    """Bersihkan nama file dari karakter tidak aman."""
    keep = "-_.() "
    return "".join(c for c in name if c.isalnum() or c in keep).strip()
