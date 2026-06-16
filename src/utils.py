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


def save_image(cv2_image, filename: str, quality: int = 80) -> str:
    """
    Simpan gambar hasil proses ke outputs/images/ dengan kompresi dan kembalikan path.
    
    Parameters
    ----------
    cv2_image : np.ndarray
        Gambar dalam format BGR (OpenCV).
    filename : str
        Nama file output.
    quality : int
        Kualitas JPEG (1-95). Default 80 untuk kompresi optimal.
    
    Returns
    -------
    str
        Path file yang disimpan.
    """
    ensure_dirs()
    path = os.path.join("outputs", "images", filename)
    
    # Convert BGR to RGB untuk Pillow
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    
    # Gunakan Pillow untuk kompresi JPEG
    from PIL import Image
    pil_image = Image.fromarray(rgb_image)
    pil_image.save(path, format='JPEG', quality=quality, optimize=True)
    
    return path


def safe_filename(name: str) -> str:
    """Bersihkan nama file dari karakter tidak aman."""
    keep = "-_.() "
    return "".join(c for c in name if c.isalnum() or c in keep).strip()


def delete_image_file(image_path: str) -> bool:
    """
    Hapus file gambar dari disk.
    
    Parameters
    ----------
    image_path : str
        Path lengkap file gambar yang akan dihapus.
    
    Returns
    -------
    bool
        True jika berhasil, False jika gagal atau file tidak ada.
    """
    try:
        if os.path.exists(image_path):
            os.remove(image_path)
            return True
        return False
    except Exception as e:
        print(f"Error menghapus file {image_path}: {e}")
        return False
