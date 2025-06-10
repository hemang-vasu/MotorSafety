from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import time

app = Flask(__name__)

# Load YOLOv8 nano model (you can download weights automatically)
model = YOLO('yolov5n.pt')

# Replace with your Akaso camera's stream URL
stream_url = "rtsp://192.168.1.1/live"
cap = cv2.VideoCapture(stream_url)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Run YOLO inference
        small_frame = cv2.resize(frame, (160, 120))  # or even (160, 120)
        results = model(small_frame)[0]  # get first (and only) result

        # Draw bounding boxes and labels
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            conf = box.conf[0]
            label = f"{model.names[cls_id]} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield frame as multipart HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.5)

@app.route('/')
def index():
    return "<h1>Raspberry Pi Live Stream</h1><img src='/video'>"

@app.route('/video')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
