import time
import cv2
import pyautogui

pyautogui.PAUSE = 0


class MediaController:
    GESTURES = {
        (1, 1, 1, 1): ("Play/Pause", "playpause"),
        (1, 0, 0, 0): ("Next track", "nexttrack"),
        (1, 1, 0, 0): ("Previous track", "prevtrack"),
    }

    def __init__(self, hold_time=0.7, cooldown=1.5):
        self.hold_time = hold_time
        self.cooldown = cooldown
        self.current = None
        self.start = 0
        self.progress = 0
        self.last_trigger = 0
        self.message = ""
        self.msg_time = 0

    def update(self, fingers):
        now = time.time()
        gesture = self.GESTURES.get(tuple(fingers[1:]))

        if gesture is None or now - self.last_trigger < self.cooldown:
            self.current, self.progress = None, 0
            return

        if gesture != self.current:
            self.current, self.start = gesture, now

        self.progress = min((now - self.start) / self.hold_time, 1)
        if self.progress >= 1:
            pyautogui.press(gesture[1])
            self.last_trigger = now
            self.message, self.msg_time = gesture[0], now
            self.current, self.progress = None, 0

    def draw(self, frame):
        for i, text in enumerate(["Open palm: Play/Pause",
                                  "Index only: Next",
                                  "Peace sign: Previous"]):
            cv2.putText(frame, text, (10, 30 + i * 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        if self.progress > 0:
            w = int(200 * self.progress)
            cv2.rectangle(frame, (10, 125), (210, 145), (255, 255, 255), 2)
            cv2.rectangle(frame, (10, 125), (10 + w, 145), (0, 255, 0), cv2.FILLED)

        if time.time() - self.msg_time < 1.5 and self.message:
            cv2.putText(frame, self.message, (10, 190),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)