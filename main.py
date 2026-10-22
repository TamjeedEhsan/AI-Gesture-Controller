import cv2
from hand_tracking import HandTracker

cap = cv2.VideoCapture(0)
tracker = HandTracker()

while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)

    frame = tracker.find_hands(frame)
    lm = tracker.get_landmarks(frame)

    if lm:
        fingers = tracker.fingers_up(lm)
        cv2.putText(frame, str(fingers), (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if fingers == [0, 1, 0, 0, 0]:
            gesture = "Pointing"
        elif fingers == [0, 1, 1, 0, 0]:
            gesture = "Two fingers"
        elif fingers == [1, 1, 1, 1, 1]:
            gesture = "Open palm"
        elif sum(fingers) == 0:
            gesture = "Fist"
        else:
            gesture = ""
        cv2.putText(frame, gesture, (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Gesture Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()