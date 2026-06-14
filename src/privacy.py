"""
privacy.py
Menyamarkan wajah menggunakan Gaussian Blur untuk melindungi privasi individu.
Output: gambar dengan wajah ter-blur.
"""

import cv2
import numpy as np


def blur_faces(image: np.ndarray, faces: list, blur_strength: int = 51) -> np.ndarray:
    """
    Menerapkan Gaussian Blur pada area wajah yang terdeteksi.

    Parameters
    ----------
    image : np.ndarray
        Gambar input dalam format BGR (OpenCV).
    faces : list of tuple
        Daftar koordinat wajah (x, y, w, h) dari detector.py.
    blur_strength : int
        Ukuran kernel Gaussian Blur (harus ganjil, makin besar makin blur).

    Returns
    -------
    np.ndarray
        Gambar dengan wajah yang sudah disamarkan (blurred).
    """
    output = image.copy()

    # Pastikan kernel ganjil dan minimal 3
    k = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
    k = max(k, 3)

    for (x, y, w, h) in faces:
        # Pastikan koordinat tidak keluar batas gambar
        x1, y1 = max(x, 0), max(y, 0)
        x2, y2 = min(x + w, output.shape[1]), min(y + h, output.shape[0])

        if x2 <= x1 or y2 <= y1:
            continue

        face_roi = output[y1:y2, x1:x2]
        blurred_roi = cv2.GaussianBlur(face_roi, (k, k), 0)
        output[y1:y2, x1:x2] = blurred_roi

    return output


def pixelate_faces(image: np.ndarray, faces: list, pixel_size: int = 10) -> np.ndarray:
    """
    Alternatif: menyamarkan wajah dengan efek pixelate (mosaic).
    Disediakan sebagai opsi tambahan privasi.
    """
    output = image.copy()

    for (x, y, w, h) in faces:
        x1, y1 = max(x, 0), max(y, 0)
        x2, y2 = min(x + w, output.shape[1]), min(y + h, output.shape[0])

        if x2 <= x1 or y2 <= y1:
            continue

        face_roi = output[y1:y2, x1:x2]
        small = cv2.resize(face_roi, (max(1, (x2 - x1) // pixel_size), max(1, (y2 - y1) // pixel_size)),
                            interpolation=cv2.INTER_LINEAR)
        mosaic = cv2.resize(small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
        output[y1:y2, x1:x2] = mosaic

    return output
