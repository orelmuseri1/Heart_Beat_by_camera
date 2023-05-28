from Camera_Stream_Receiver import CameraStreamReceiver
from Frame_processor import FaceRecognizer
from Detector import PulseDetector
import cv2
import time

Greens = []
PULSE_TO_COUNTER_PER_UPDATE = 10
def check_time_elapsed(start_time):
    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time

def calculate_average(data):
    total = sum(data)
    count = len(data)
    if count >2:
        average = total / count
        return average
    else:
        return None

if __name__ == '__main__':
    receiver = CameraStreamReceiver()
    face_recognizer = FaceRecognizer()
    receiver.start()
    start_time = time.time()
    counter_pulse = 0
    count =True # Flag so we know we count this pulse to ignor next frame
    while True:
        # Get a frame from the camera stream
        frame = receiver.get_stream()

        # If a frame is received, process it with the face recognizer
        if frame is not None:
            new_green = face_recognizer.process_frame(frame)
            elapsed = check_time_elapsed(start_time)
            #print("time: " + str(elapsed))
            if new_green != None:
                Greens.append(new_green)
                AVRGE = calculate_average(Greens)
                if AVRGE != None:
                    #print("AVRGE: " + str(AVRGE))
                    if new_green+1 < AVRGE and count:
                        counter_pulse += 1
                        count = False
                    elif new_green-1 > AVRGE and not count:
                        count =True
                    if counter_pulse>= PULSE_TO_COUNTER_PER_UPDATE:
                        counter_pulse =0
                        Pulse = PULSE_TO_COUNTER_PER_UPDATE*60/elapsed
                        start_time = time.time()
                        print("Pulse: " + str(int(Pulse)))

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            receiver.close_stream()
            break

    filtered_Greens = list(filter(lambda x: x is not None, Greens))
    pulse_detector = PulseDetector(filtered_Greens)
    pulse_detector.show()

