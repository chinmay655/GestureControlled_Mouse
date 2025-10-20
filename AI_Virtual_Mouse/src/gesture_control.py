import numpy as np
import time

class GestureController:
    def __init__(self):
        # thresholds (normalized distances)
        self.click_threshold = 40        # pixels (tweak if needed)
        self.drag_threshold = 45
        self.right_click_threshold = 40
        self.screenshot_threshold = 40
        self.last_click_time = 0
        self.click_cooldown = 0.3  # seconds
        self.screenshot_cooldown = 1.0  # prevent multiple screenshots

    def _distance(self, p1, p2):
        return np.hypot(p1['x'] - p2['x'], p1['y'] - p2['y'])

    def recognize_gesture(self, landmarks, frame=None):
        """Return a dictionary describing the gesture and relevant parameters."""
        if not landmarks:
            return {'action': 'none'}

        # fingertip indices in mediapipe: thumb=4, index=8, middle=12, ring=16, pinky=20
        thumb = landmarks[4]
        index = landmarks[8]
        middle = landmarks[12]
        ring = landmarks[16]

        # distances
        idx_thumb = self._distance(index, thumb)
        mid_thumb = self._distance(middle, thumb)
        idx_mid = self._distance(index, middle)
        idx_ring = self._distance(index, ring)

        # Detect screenshot: index+middle+ring close together
        if idx_mid < self.screenshot_threshold and idx_ring < self.screenshot_threshold:
            now = time.time()
            if now - self.last_click_time > self.screenshot_cooldown:
                self.last_click_time = now
                return {'action': 'screenshot'}

        # Left click: index + thumb close
        if idx_thumb < self.click_threshold:
            now = time.time()
            if now - self.last_click_time > self.click_cooldown:
                self.last_click_time = now
                return {'action': 'left_click'}

        # Right click: middle + thumb close
        if mid_thumb < self.right_click_threshold:
            return {'action': 'right_click'}

        # Drag: index + middle close (and held)
        if idx_mid < self.drag_threshold:
            return {'action': 'drag'}

        # Volume control gesture: pinch-like but based on index-thumb distance > threshold
        # We'll indicate volume control when index and thumb are apart but roughly aligned vertically
        # (Caller will interpret distances)
        return {'action': 'move', 'index': index, 'thumb': thumb, 'distance_idx_thumb': idx_thumb}
