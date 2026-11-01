import cv2
import numpy as np
import pyautogui

pyautogui.PAUSE = 0

class MouseController:
    def __init__(self, frame_w, frame_h, margin=100, smoothing=5):
        self.frame_w, self.frame_h = frame_w, frame_h
        self.margin = margin          
        self.smoothing = smoothing    
        self.screen_w, self.screen_h = pyautogui.size()
        self.prev_x, self.prev_y = pyautogui.position()
        self.was_pinching = False

    def update(self, x, y, pinching):
        sx = np.interp(x, (self.margin, self.frame_w - self.margin), (5, self.screen_w - 5))
        sy = np.interp(y, (self.margin, self.frame_h - self.margin), (5, self.screen_h - 5))

        if not pinching:
            cur_x = self.prev_x + (sx - self.prev_x) / self.smoothing
            cur_y = self.prev_y + (sy - self.prev_y) / self.smoothing
            pyautogui.moveTo(cur_x, cur_y)
            self.prev_x, self.prev_y = cur_x, cur_y
        elif not self.was_pinching:
            pyautogui.click()   

        self.was_pinching = pinching

    def draw(self, frame):
        m = self.margin
        cv2.rectangle(frame, (m, m), (self.frame_w - m, self.frame_h - m), (255, 0, 255), 2)