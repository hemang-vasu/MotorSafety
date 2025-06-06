import cv2

# RTSP stream URL, safe for github since its a local IP for testing purposes of a camera
stream_url = "rtsp://192.168.1.1/live"

# Open video capture from the stream
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Display the frame
    cv2.imshow('AKASO Live Stream', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release and close windows
cap.release()
cv2.destroyAllWindows()