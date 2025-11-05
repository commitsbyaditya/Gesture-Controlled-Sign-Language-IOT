import cv2
from ultralytics import YOLO
import mediapipe as mp

# ---------- YOLO SIGN MODEL ----------
MODEL_PATH = "./best.pt"  # your trained model path
model = YOLO(MODEL_PATH)

# ---------- FACE DETECTION ----------
mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(min_detection_confidence=0.6)

# ---------- CAMERA SETUP ----------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip for mirror view
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    # ---------- SIGN DETECTION (YOLO) ----------
    results = model.predict(frame, conf=0.5, verbose=False)
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]
            # Draw sign box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, f"{label} {conf:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # ---------- FACE DETECTION (MEDIAPIPE) ----------
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_results = face_detector.process(img_rgb)

    if face_results.detections:
        for det in face_results.detections:
            bbox = det.location_data.relative_bounding_box
            xmin = int(bbox.xmin * w)
            ymin = int(bbox.ymin * h)
            box_w = int(bbox.width * w)
            box_h = int(bbox.height * h)
            xmax = xmin + box_w
            ymax = ymin + box_h
            conf_face = det.score[0]

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, f"Face {conf_face:.2f}",
                        (xmin, ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # (Optional) Extract face crop for emotion model
            face_crop = frame[ymin:ymax, xmin:xmax].copy()
            # Here you can later send face_crop to an emotion classification model

    # ---------- DISPLAY ----------
    cv2.imshow("Sign + Face Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()