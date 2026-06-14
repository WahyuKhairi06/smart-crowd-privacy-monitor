"""
analytics.py
Menghitung jumlah wajah dan mengklasifikasikan tingkat kepadatan keramaian.

Rule klasifikasi kepadatan:
    0 - 5   -> Low
    6 - 15  -> Medium
    > 15    -> High
"""

# Konfigurasi ambang batas (threshold) klasifikasi kepadatan
DENSITY_THRESHOLDS = {
    "Low": (0, 5),
    "Medium": (6, 15),
    "High": (16, float("inf")),
}

# Warna representatif untuk tiap level (selaras dengan tema dashboard)
DENSITY_COLORS = {
    "Low": "#27AE60",     # Success / hijau
    "Medium": "#FFD23F",  # Accent Gold
    "High": "#EF6C4A",    # Coral
}

# Emoji representatif untuk tiap level
DENSITY_EMOJI = {
    "Low": "🟢",
    "Medium": "🟡",
    "High": "🔴",
}


def count_faces(faces: list) -> int:
    """Menghitung jumlah wajah yang terdeteksi."""
    return len(faces)


def classify_density(face_count: int) -> str:
    """
    Mengklasifikasikan tingkat kepadatan keramaian berdasarkan jumlah wajah.

    Parameters
    ----------
    face_count : int
        Jumlah wajah yang terdeteksi pada gambar.

    Returns
    -------
    str
        Salah satu dari: "Low", "Medium", "High".
    """
    if face_count <= 5:
        return "Low"
    elif face_count <= 15:
        return "Medium"
    else:
        return "High"


def get_density_color(level: str) -> str:
    """Mengembalikan kode warna hex untuk level kepadatan tertentu."""
    return DENSITY_COLORS.get(level, "#2BA8A2")


def get_density_emoji(level: str) -> str:
    """Mengembalikan emoji representatif untuk level kepadatan tertentu."""
    return DENSITY_EMOJI.get(level, "⚪")


def analyze(faces: list) -> dict:
    """
    Menjalankan analisis lengkap: hitung wajah & klasifikasi kepadatan.

    Returns
    -------
    dict
        {
            "face_count": int,
            "density_level": str,
            "density_color": str,
            "density_emoji": str,
        }
    """
    face_count = count_faces(faces)
    density_level = classify_density(face_count)

    return {
        "face_count": face_count,
        "density_level": density_level,
        "density_color": get_density_color(density_level),
        "density_emoji": get_density_emoji(density_level),
    }
