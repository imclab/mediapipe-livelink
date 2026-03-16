from __future__ import annotations

from math import atan2, degrees, hypot
from typing import Iterable


def _point(landmark: dict) -> tuple[float, float, float]:
    return float(landmark["x"]), float(landmark["y"]), float(landmark.get("z", 0.0))


def _distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return hypot(a[0] - b[0], a[1] - b[1])


def summarize_face_landmarks(landmarks: Iterable[dict]) -> dict:
    """Return lightweight spatial intelligence from MediaPipe-style landmarks.

    Expects at least landmarks for eyes and nose:
    - left eye outer corner idx 33
    - right eye outer corner idx 263
    - nose tip idx 1
    """
    pts = list(landmarks)
    if len(pts) < 264:
        return {"status": "insufficient_landmarks", "message": "Need full face mesh landmarks."}

    left_eye = _point(pts[33])
    right_eye = _point(pts[263])
    nose = _point(pts[1])

    eye_center = ((left_eye[0] + right_eye[0]) / 2, (left_eye[1] + right_eye[1]) / 2, 0.0)
    eye_distance = _distance(left_eye, right_eye)
    yaw_vector = nose[0] - eye_center[0]
    yaw_normalized = yaw_vector / eye_distance if eye_distance else 0.0

    roll_radians = atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
    roll_deg = degrees(roll_radians)

    attention = "center"
    if yaw_normalized > 0.06:
        attention = "looking_right"
    elif yaw_normalized < -0.06:
        attention = "looking_left"

    if abs(roll_deg) > 12:
        attention += "_head_tilted"

    return {
        "status": "ok",
        "attention": attention,
        "roll_deg": round(roll_deg, 2),
        "yaw_normalized": round(yaw_normalized, 3),
    }
