import cv2
FONT = cv2.FONT_HERSHEY_SIMPLEX

class InstructionsPanel:
    LINES = [
        ("D", "Draw mode"),
        ("K", "Keyboard mode"),
        ("M", "Mouse mode"),
        ("V", "Volume mode"),
        ("Z", "Zoom mode"),
        ("P", "Media mode"),
        ("C", "Clear canvas"),
        ("S", "Save drawing"),
        ("I", "Show/hide instructions"),
        ("Q", "Quit"),
    ]

    def __init__(self, frame_w, frame_h, btn_w=150, btn_h=40, margin=10):
        self.btn = (frame_w - btn_w - margin, frame_h - btn_h - margin,
                    frame_w - margin, frame_h - margin)   #
        self.visible = False

    def toggle(self):
        self.visible = not self.visible

    def on_mouse(self, event, x, y, flags, param):
        """OpenCV calls this on every mouse event in the window."""
        if event == cv2.EVENT_LBUTTONDOWN:
            x1, y1, x2, y2 = self.btn
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.toggle()

    def _draw_panel(self, frame):
        row_h, pad, panel_w = 30, 15, 340
        panel_h = 30 + row_h * len(self.LINES)
        bx1, by1, bx2, by2 = self.btn
        x2, y2 = bx2, by1 - 10
        x1, y1 = x2 - panel_w, y2 - panel_h

        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (30, 30, 30), cv2.FILLED)
        cv2.addWeighted(overlay, 0.9, frame, 0.1, 0, frame)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

        for i, (key, text) in enumerate(self.LINES):
            y = y1 + 35 + i * row_h
            cv2.putText(frame, key, (x1 + pad, y), FONT, 0.65, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, text, (x1 + pad + 40, y), FONT, 0.65, (255, 255, 255), 2, cv2.LINE_AA)

    def draw(self, frame):
        if self.visible:
            self._draw_panel(frame)

        x1, y1, x2, y2 = self.btn
        color = (0, 140, 0) if self.visible else (70, 70, 70)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FILLED)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.putText(frame, "Instructions", (x1 + 12, y1 + 27), FONT, 0.6, (255, 255, 255), 2, cv2.LINE_AA)