import cv2
from ultralytics import YOLO
import time

# Load lightweight YOLOv8n model
model = YOLO('yolov8n.pt')

# RTSP stream URL
stream_url = "rtsp://192.168.1.1/live"
cap = cv2.VideoCapture(stream_url)

cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
cap.set(cv2.CAP_PROP_FPS, 30)

frame_count = 0
last_time = time.time()
last_results = None  # To store last detections

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to read frame")
        break

    frame_count += 1

    # Only run YOLO every 15 frames
    if frame_count % 15 == 0:
        results = model(frame, verbose=False)[0]
        last_results = results  # Cache results
    else:
        results = last_results  # Use previous detections

    # Draw cached detections
    if results:
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = f"{model.names[cls_id]} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("YOLOv8n RTSP Stream", frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Optional: print FPS
    if time.time() - last_time >= 1.0:
        print(f"FPS: {frame_count}")
        frame_count = 0
        last_time = time.time()

cap.release()
cv2.destroyAllWindows()
