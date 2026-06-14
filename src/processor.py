"""
processor.py
Pipeline proses gambar end-to-end:
    Upload -> Face Detection (Haar Cascade) -> Gaussian Blur ->
    Face Counting -> Density Classification -> Save & Log
"""

from src.detector import detect_faces
from src.privacy import blur_faces
from src.analytics import analyze
from src.utils import save_image, timestamp_now, safe_filename
from src.storage import save_record


def process_image(cv2_image, original_filename: str, blur_strength: int = 51) -> dict:
    """
    Menjalankan seluruh pipeline analisis pada satu gambar.

    Parameters
    ----------
    cv2_image : np.ndarray
        Gambar input dalam format BGR (OpenCV).
    original_filename : str
        Nama file asli yang diunggah pengguna.
    blur_strength : int
        Kekuatan kernel Gaussian Blur.

    Returns
    -------
    dict
        {
            "protected_image": np.ndarray,  # gambar hasil blur (BGR)
            "faces": list,                  # koordinat wajah terdeteksi
            "face_count": int,
            "density_level": str,
            "density_color": str,
            "density_emoji": str,
            "timestamp": str,
            "saved_path": str,
        }
    """
    # 1. Face Detection (Haar Cascade + profile) — expand boxes to cover heads/hats
    faces = detect_faces(cv2_image, expand_head=True)

    # 2. Gaussian Blur (Privacy Protection)
    protected_image = blur_faces(cv2_image, faces, blur_strength=blur_strength)

    # 3 & 4. Face Counting & Density Classification
    result = analyze(faces)

    # 5. Simpan gambar hasil & catat ke histori
    ts = timestamp_now()
    safe_name = safe_filename(original_filename) or "image.jpg"
    out_filename = f"{ts}_{safe_name}"
    saved_path = save_image(protected_image, out_filename)

    save_record(
        timestamp=ts,
        filename=safe_name,
        face_count=result["face_count"],
        density_level=result["density_level"],
        image_path=saved_path,
    )

    return {
        "protected_image": protected_image,
        "faces": faces,
        "face_count": result["face_count"],
        "density_level": result["density_level"],
        "density_color": result["density_color"],
        "density_emoji": result["density_emoji"],
        "timestamp": ts,
        "saved_path": saved_path,
    }
