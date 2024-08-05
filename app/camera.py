import cv2

def capture_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

    cap.release()
    cv2.destroyAllWindows()
