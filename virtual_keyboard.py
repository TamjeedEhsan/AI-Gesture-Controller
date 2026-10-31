import cv2

class VirtualKeyboard:
    def __init__(self, frame_w, top=70, key_h=60):
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        key_w = frame_w // 11
        self.keys = []  

        for r, row in enumerate(rows):
            x0 = (frame_w - len(row) * key_w) // 2
            y1 = top + r * key_h
            for i, ch in enumerate(row):
                x1 = x0 + i * key_w
                self.keys.append((ch, x1, y1, x1 + key_w, y1 + key_h))

        y1 = top + 3 * key_h
        x0 = (frame_w - 7 * key_w) // 2
        self.keys.append(("SPACE", x0, y1, x0 + 5 * key_w, y1 + key_h))
        self.keys.append(("BACK", x0 + 5 * key_w, y1, x0 + 7 * key_w, y1 + key_h))

        self.text = ""
        self.hover = None
        self.was_pinching = False
        self.flash = 0  

    def _key_at(self, x, y):
        for label, x1, y1, x2, y2 in self.keys:
            if x1 <= x < x2 and y1 <= y < y2:
                return label
        return None

    def _press(self, label):
        if label == "BACK":
            self.text = self.text[:-1]
        elif label == "SPACE":
            self.text += " "
        else:
            self.text += label

    def update(self, x, y, pinching):
        if not pinching:
            self.hover = self._key_at(x, y)
        elif not self.was_pinching and self.hover:
            self._press(self.hover)
            self.flash = 6
        self.was_pinching = pinching

    def draw(self, frame):
        overlay = frame.copy()
        for label, x1, y1, x2, y2 in self.keys:
            color = (90, 90, 90)
            if label == self.hover:
                color = (0, 255, 0) if self.flash > 0 else (0, 200, 255)
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, cv2.FILLED)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)  # semi-transparent keys

        for label, x1, y1, x2, y2 in self.keys:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200, 200), 1)
            cv2.putText(frame, label, (x1 + 8, y1 + 38),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.rectangle(frame, (0, 0), (frame.shape[1], 50), (40, 40, 40), cv2.FILLED)
        cv2.putText(frame, self.text[-30:] + "|", (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        if self.flash > 0:
            self.flash -= 1