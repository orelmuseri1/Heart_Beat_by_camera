import face_recognition
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np

def show_color(color):
    # Create separate plots for each color channel
    fig, axs = plt.subplots(1, 3, figsize=(9, 3))

    # Iterate over each color channel
    for i in range(3):
        # Create an array of zeros with the same shape as the color
        channel = np.zeros_like(color)
        # Set the current color channel to the corresponding value
        channel[i] = color[i]
        # Set the background color of the plot
        axs[i].set_facecolor(channel / 255)
        # Remove axis ticks and labels
        axs[i].set_xticks([])
        axs[i].set_yticks([])

    # Adjust spacing between subplots
    plt.tight_layout()

    # Show the plot
    plt.show()

def get_pixel_color(frame, x, y):
    pixel = frame[y, x]
    return pixel

def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return int(distance)

def get_lowest_point(points):
    lowest_point = points[0]  # Assume the first point is the lowest

    for point in points:
        if point[1] > lowest_point[1]:
            lowest_point = point

    return lowest_point

class FaceRecognizer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def print_faces(self,frame,faces):

        # If no faces are detected, send a message
        if len(faces) == 0:
            print("No face detected")

        # Draw rectangles around the detected facesq
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_image = frame[y:y+h, x:x+w]

            face_landmarks = face_recognition.face_landmarks(face_image)
            #print(face_landmarks)
            for landmarks in face_landmarks:
                for item in landmarks:
                    #for dot in landmarks[item]:
                    #    x_mark, y_mark = dot
                    #    cv2.circle(frame, (x + x_mark, y + y_mark), 5, (30, 30, 240), -1)
                    if item == "chin1":
                        dot_left=landmarks[item][0]
                        dot_right=landmarks[item][-1]
                        x_mark_right,y_mark_right =dot_right
                        x_mark_left,y_mark_left =dot_left
                        x_mark_mid= x_mark_left + ((x_mark_right-x_mark_left)/2)
                        y_mark_mid= y_mark_left + ((y_mark_right-y_mark_left)/2)
                        dest_lowest_eyeBrows =calculate_distance((x_mark_mid, y_mark_mid), get_lowest_point(landmarks[item]))
                        y_mark_mif_forehead=y_mark_mid-dest_lowest_eyeBrows/4
                        #cv2.circle(frame, (x+int(x_mark_mid),y+int(y_mark_mif_forehead)), 5, (50, 30, 240), -1)

                        color = get_pixel_color(frame, x+int(x_mark_mid), y+int(y_mark_mif_forehead))
                        #print(color)
                        return color[1] #retunr only the grean of the first face instead of everyone!
                        #show_color(color)



    def detect_face_landmarks(self, rgb_frame):
        face_landmarks = face_recognition.face_landmarks(rgb_frame)
        return face_landmarks

    def process_frame(self, frame):
        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        #print markes of faces
        green = self.print_faces(frame, faces)

        # Display the frame
        cv2.imshow('Face Recognition', frame)
        cv2.waitKey(1)
        return green