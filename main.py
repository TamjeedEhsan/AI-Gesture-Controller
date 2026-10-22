import cv2
import numpy as np
from hand_tracking import HandTracker

cap = cv2.VideoCapture(0)
tracker = HandTracker()

canvas = None
prev = None                 # last fingertip position while drawing
draw_color = (0, 0, 255)    # BGR, so this is red
thickness = 6

while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    frame = tracker.find_hands(frame)
    lm = tracker.get_landmarks(frame)

    if lm:
        fingers = tracker.fingers_up(lm)
        x, y = lm[8][1], lm[8][2]   # index fingertip

        # Pen down: index up, middle down (thumb is ignored, it's the least reliable)
        if fingers[1] == 1 and fingers[2] == 0:
            if prev is None:
                prev = (x, y)
            cv2.line(canvas, prev, (x, y), draw_color, thickness)
            prev = (x, y)
            cv2.circle(frame, (x, y), 10, draw_color, cv2.FILLED)
        else:
            prev = None
    else:
        prev = None

    # Overlay the canvas on the live frame
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    mask = gray > 0
    frame[mask] = canvas[mask]

    cv2.imshow("Gesture Controller", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()