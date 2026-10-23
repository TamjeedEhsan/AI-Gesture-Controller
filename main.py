import cv2
import numpy as np
from hand_tracking import HandTracker
from color_picker import ColorPicker

cap = cv2.VideoCapture(0)
tracker = HandTracker()
picker = ColorPicker(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))

canvas = None
prev = None

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

        if fingers[1] == 1 and fingers[2] == 1:
            # Selection mode: hover and pick, no drawing
            prev = None
            picker.select(x, y)
            cv2.circle(frame, (x, y), 12, (255, 255, 255), 2)

        elif fingers[1] == 1 and fingers[2] == 0:
            # Draw mode (ignore the palette area)
            if y > picker.height:
                if prev is None:
                    prev = (x, y)
                cv2.line(canvas, prev, (x, y), picker.color, picker.thickness)
                prev = (x, y)
                cv2.circle(frame, (x, y), 10, (255, 255, 255), 2)
            else:
                prev = None
        else:
            prev = None
    else:
        prev = None

    # Overlay the canvas, then the palette on top
    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY) > 0
    frame[mask] = canvas[mask]
    picker.draw(frame)

    cv2.imshow("Gesture Controller", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros_like(frame)

cap.release()
cv2.destroyAllWindows()