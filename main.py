import cv2
import numpy as np
from hand_tracking import HandTracker
from color_picker import ColorPicker
from virtual_keyboard import VirtualKeyboard
from mouse_control import MouseController

cap = cv2.VideoCapture(0)
tracker = HandTracker()
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
picker = ColorPicker(W)
keyboard = VirtualKeyboard(W)
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
mouse = MouseController(W, H)

mode = "draw"   
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

    if mode == "draw":
        if lm:
            fingers = tracker.fingers_up(lm)
            x, y = lm[8][1], lm[8][2]

            if fingers[1] == 1 and fingers[2] == 1:
                prev = None
                picker.select(x, y)
                cv2.circle(frame, (x, y), 12, (255, 255, 255), 2)
            elif fingers[1] == 1 and fingers[2] == 0:
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

        mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY) > 0
        frame[mask] = canvas[mask]
        picker.draw(frame)

    elif mode == "keyboard":
        if lm:
            x, y = lm[8][1], lm[8][2]
            palm = tracker.distance(lm, 0, 9)
            pinching = tracker.distance(lm, 4, 8) < 0.3 * palm
            keyboard.update(x, y, pinching)
            cv2.circle(frame, (x, y), 8, (255, 255, 255), cv2.FILLED)
        else:
            keyboard.update(-1, -1, False)
        keyboard.draw(frame)
    elif mode == "mouse":
        mouse.draw(frame)
        if lm:
            x, y = lm[8][1], lm[8][2]
            palm = tracker.distance(lm, 0, 9)
            pinching = tracker.distance(lm, 4, 8) < 0.3 * palm
            mouse.update(x, y, pinching)
            cv2.circle(frame, (x, y), 8, (255, 0, 255), cv2.FILLED)

    cv2.putText(frame, f"Mode: {mode}", (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("Gesture Controller", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros_like(frame)
    elif key == ord('d'):
        mode, prev = "draw", None
    elif key == ord('k'):
        mode, prev = "keyboard", None
    elif key == ord('m'):
        mode, prev = "mouse", None

cap.release()
cv2.destroyAllWindows()