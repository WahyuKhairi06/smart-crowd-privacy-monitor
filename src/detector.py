"""
detector.py
Deteksi wajah menggunakan Haar Cascade (OpenCV).
Output: list koordinat wajah (x, y, w, h)
"""

import cv2
import numpy as np
from typing import List, Tuple


# Load Haar Cascade default OpenCV (frontal face)
_FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
_PROFILE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_profileface.xml"

_face_cascade = cv2.CascadeClassifier(_FACE_CASCADE_PATH)
_profile_cascade = cv2.CascadeClassifier(_PROFILE_CASCADE_PATH)


def detect_faces(image: np.ndarray,
                 scale_factor: float = 1.1,
                 min_neighbors: int = 5,
                 min_size: tuple = (30, 30),
                 expand_head: bool = True,
                 expand_top_ratio: float = 0.6,
                 expand_lr_ratio: float = 0.15,
                 iou_threshold: float = 0.3) -> Tuple[List[Tuple[int, int, int, int]], float]:
    """
    Mendeteksi wajah pada gambar menggunakan Haar Cascade.

    Parameters
    ----------
    image : np.ndarray
        Gambar input dalam format BGR (OpenCV).
    scale_factor : float
        Parameter scaling Haar Cascade.
    min_neighbors : int
        Minimum neighbor untuk validasi deteksi.
    min_size : tuple
        Ukuran minimum wajah yang dideteksi (px).

    Returns
    -------
    list of tuple
        Daftar koordinat wajah (x, y, w, h).
    """
    if image is None:
        return [], 0.0

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    rects = []

    # frontal faces
    faces = _face_cascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=min_size,
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    rects.extend([tuple(map(int, f)) for f in faces])

    # profile faces (helps when head is rotated or partially occluded)
    profiles = _profile_cascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=max(3, min_neighbors - 2),
        minSize=min_size,
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    rects.extend([tuple(map(int, p)) for p in profiles])

    if not rects:
        return [], 0.0

    # merge overlapping rects (simple union for overlapping detections)
    merged = _merge_rects(rects, iou_threshold=iou_threshold)
    confidence = _compute_confidence(merged, image.shape)

    # optionally expand bbox upward/sideways to cover full head and hats
    if expand_head:
        expanded = [_expand_bbox(r, image.shape, expand_top_ratio, expand_lr_ratio) for r in merged]
        return [tuple(map(int, r)) for r in expanded], confidence

    return [tuple(map(int, r)) for r in merged], confidence


def _expand_bbox(bbox: Tuple[int, int, int, int], image_shape: tuple, top_ratio: float, lr_ratio: float) -> Tuple[int, int, int, int]:
    """Perluas bounding box ke atas dan ke samping untuk meliputi kepala/topi."""
    x, y, w, h = bbox
    img_h, img_w = image_shape[0], image_shape[1]

    extra_top = int(h * top_ratio)
    extra_lr = int(w * lr_ratio)

    x1 = max(0, x - extra_lr)
    y1 = max(0, y - extra_top)
    x2 = min(img_w, x + w + extra_lr)
    y2 = min(img_h, y + h)

    return (x1, y1, x2 - x1, y2 - y1)


def _merge_rects(rects: List[Tuple[int, int, int, int]], iou_threshold: float = 0.3) -> List[Tuple[int, int, int, int]]:
    """Merge rectangles that overlap by IoU > threshold by taking their union."""
    if not rects:
        return []

    rects = [tuple(map(int, r)) for r in rects]
    used = [False] * len(rects)
    merged = []

    for i, r in enumerate(rects):
        if used[i]:
            continue
        x1, y1, w1, h1 = r
        rx1, ry1, rx2, ry2 = x1, y1, x1 + w1, y1 + h1
        used[i] = True

        for j in range(i + 1, len(rects)):
            if used[j]:
                continue
            x2, y2, w2, h2 = rects[j]
            sx1, sy1, sx2, sy2 = x2, y2, x2 + w2, y2 + h2
            iou = _rect_iou((rx1, ry1, rx2, ry2), (sx1, sy1, sx2, sy2))
            if iou > iou_threshold:
                # union
                rx1 = min(rx1, sx1)
                ry1 = min(ry1, sy1)
                rx2 = max(rx2, sx2)
                ry2 = max(ry2, sy2)
                used[j] = True

        merged.append((rx1, ry1, rx2 - rx1, ry2 - ry1))

    return merged



def _rect_iou(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_x1 = max(ax1, bx1)
    inter_y1 = max(ay1, by1)
    inter_x2 = min(ax2, bx2)
    inter_y2 = min(ay2, by2)
    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h
    area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    area_b = max(0, bx2 - bx1) * max(0, by2 - by1)
    union = area_a + area_b - inter_area
    if union == 0:
        return 0.0
    return inter_area / union


def _compute_confidence(rects: List[Tuple[int, int, int, int]], image_shape: tuple) -> float:
    """Hitung confidence score sederhana berdasarkan ukuran relatif deteksi wajah."""
    if not rects:
        return 0.0
    img_h, img_w = image_shape[0], image_shape[1]
    image_area = max(1, img_w * img_h)

    # Rasio luas rata-rata bbox terhadap luas gambar
    ratios = []
    for x, y, w, h in rects:
        box_area = max(1, w * h)
        ratios.append(box_area / image_area)

    avg_ratio = sum(ratios) / len(ratios)

    # size_score: lebih besar jika bbox relatif cukup besar (baseline ~0.8%)
    size_score = min(1.0, avg_ratio / 0.008)

    # face_count_factor: memberi poin lebih jika sejumlah wajah terdeteksi (0..5+)
    face_count_factor = min(1.0, len(rects) / 5.0)

    # Kombinasi heuristik — ukuran lebih penting, jumlah juga berkontribusi
    confidence = size_score * 0.6 + face_count_factor * 0.4

    return float(round(min(max(confidence * 100.0, 0.0), 100.0), 1))


def draw_face_boxes(image: np.ndarray, faces: list, color=(0, 255, 0), thickness=2) -> np.ndarray:
    """
    Menggambar kotak deteksi wajah pada gambar (opsional, untuk debugging/preview).
    """
    output = image.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(output, (x, y), (x + w, y + h), color, thickness)
    return output
