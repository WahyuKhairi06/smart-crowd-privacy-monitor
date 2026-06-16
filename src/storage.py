"""
storage.py
Menyimpan & memuat histori hasil analisis ke/dari data/analytics.csv
"""

import os
import pandas as pd

CSV_PATH = os.path.join("data", "analytics.csv")

COLUMNS = ["timestamp", "filename", "face_count", "density_level", "image_path"]


def init_storage():
    """Inisialisasi file CSV histori jika belum ada."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_PATH, index=False)


def save_record(timestamp: str, filename: str, face_count: int,
                 density_level: str, image_path: str) -> None:
    """Menambahkan satu baris record hasil analisis ke histori."""
    init_storage()

    new_row = pd.DataFrame([{
        "timestamp": timestamp,
        "filename": filename,
        "face_count": face_count,
        "density_level": density_level,
        "image_path": image_path,
    }])

    df = pd.read_csv(CSV_PATH)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)


def load_history() -> pd.DataFrame:
    """Memuat seluruh histori analisis sebagai DataFrame."""
    init_storage()
    df = pd.read_csv(CSV_PATH)

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values("timestamp", ascending=False).reset_index(drop=True)

    return df


def clear_history() -> None:
    """
    Menghapus seluruh histori (reset CSV) dan menghapus semua file gambar dari server.
    """
    from src.utils import delete_image_file
    
    # Baca data lama untuk mendapatkan path gambar
    try:
        df = pd.read_csv(CSV_PATH)
        # Hapus semua file gambar
        if not df.empty:
            for image_path in df["image_path"]:
                delete_image_file(image_path)
    except Exception as e:
        print(f"Error saat membaca CSV untuk menghapus gambar: {e}")
    
    # Reset CSV
    df = pd.DataFrame(columns=COLUMNS)
    df.to_csv(CSV_PATH, index=False)
