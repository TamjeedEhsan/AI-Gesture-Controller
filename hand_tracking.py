import math
import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_conf=0.7, tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.results = None

    def find_hands(self, frame, draw=True):
        """Run detection on a frame; optionally draw the skeleton."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        if draw and self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_landmarks(self, frame, hand_no=0):
        """Return a list of [id, x, y] in pixels for one hand (empty if none)."""
        landmarks = []
        if self.results and self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            h, w, _ = frame.shape
            for i, lm in enumerate(hand.landmark):
                landmarks.append([i, int(lm.x * w), int(lm.y * h)])
        return landmarks

    def fingers_up(self, lm):
        """Return [thumb, index, middle, ring, pinky] as 1 (up) or 0 (down)."""
        if not lm:
            return []

        def dist(a, b):
            return math.hypot(lm[a][1] - lm[b][1], lm[a][2] - lm[b][2])

        fingers = []
        # Thumb: tip (4) farther from pinky base (17) than the joint below it (3)
        fingers.append(1 if dist(4, 17) > dist(3, 17) else 0)
        # Other fingers: tip (8,12,16,20) above the joint two points below it
        for tip in [8, 12, 16, 20]:
            fingers.append(1 if lm[tip][2] < lm[tip - 2][2] else 0)
        return fingers

    def distance(self, lm, a, b):
        """Pixel distance between landmarks a and b."""
        return math.hypot(lm[a][1] - lm[b][1], lm[a][2] - lm[b][2])