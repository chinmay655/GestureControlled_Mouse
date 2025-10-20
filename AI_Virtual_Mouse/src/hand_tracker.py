import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, max_hands=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.max_hands = max_hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        multi_landmarks = results.multi_hand_landmarks
        if multi_landmarks:
            for handLms in multi_landmarks:
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)
        # Convert landmarks to a friendly list of dicts (if present)
        if not multi_landmarks:
            return None
        # return first hand's normalized landmarks
        hand = multi_landmarks[0].landmark
        # convert to list of (x,y) in pixel coords
        h, w, _ = frame.shape
        coords = []
        for lm in hand:
            coords.append({'x': int(lm.x * w), 'y': int(lm.y * h), 'nx': lm.x, 'ny': lm.y})
        return coords
