from flask import Flask, Response
import cv2

app = Flask(__name__)

# Replace with your Akaso camera's stream URL
stream_url = "rtsp://192.168.1.1/live"
cap = cv2.VideoCapture(stream_url)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "<h1>Raspberry Pi Live Stream</h1><img src='/video'>"

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
