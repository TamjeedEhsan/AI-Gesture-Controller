import cv2

cap = cv2.VideoCapture(0)  # 0 = default webcam

while True:
    success, frame = cap.read()
    if not success:
        break
    frame = cv2.flip(frame, 1)  # mirror it so movement feels natural
    cv2.imshow("Gesture Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()