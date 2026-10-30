import cv2
import numpy as np


class ZoomController:
    def __init__(self, min_ratio=0.25, max_ratio=1.4, max_zoom=5.0):
        self.level = 1.0
        self.min_ratio, self.max_ratio = min_ratio, max_ratio
        self.max_zoom = max_zoom

    def update(self, ratio, locked):
        if locked:
            return
        target = float(np.interp(ratio, (self.min_ratio, self.max_ratio), (1.0, self.max_zoom)))
        self.level += (target - self.level) * 0.2     # smoothing

    def apply(self, frame):
        if self.level <= 1.01:
            return frame
        h, w = frame.shape[:2]
        new_w, new_h = int(w / self.level), int(h / self.level)
        x1, y1 = (w - new_w) // 2, (h - new_h) // 2
        crop = frame[y1:y1 + new_h, x1:x1 + new_w]
        return cv2.resize(crop, (w, h))

    def draw(self, frame):
        cv2.putText(frame, f"Zoom: {self.level:.1f}x", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)