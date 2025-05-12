import cv2
from ultralytics import YOLO

# Optional: Color correction using CLAHE
def correct_color(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    corrected = cv2.merge((cl, a, b))
    return cv2.cvtColor(corrected, cv2.COLOR_LAB2BGR)

def start_detection():
    model = YOLO("yolov8s.pt")  # Download first if needed
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        corrected = correct_color(frame)
        results = model(corrected, imgsz=640, verbose=False)
        annotated = results[0].plot()

        cv2.imshow("YOLOv8s Detection", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_detection()
