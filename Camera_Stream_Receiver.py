import cv2

class CameraStreamReceiver:
    def __init__(self):
        self.cap = None

    def start(self):
        # Open the default webcam
        self.cap = cv2.VideoCapture(0)

        # Check if the webcam is successfully opened
        if not self.cap.isOpened():
            print("Failed to open webcam")
            return
    def get_stream(self):
        # Check if the webcam is successfully opened
        if not self.cap.isOpened():
            print("Failed to open webcam")
            return
        ret, frame = self.cap.read()
        if ret:
            #cv2.imshow('Webcam', frame)
            return frame
        else:
            return None

    def close_stream(self):
        # Release the webcam and close the window
        self.cap.release()
        cv2.destroyAllWindows()

