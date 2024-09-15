import mediapipe as mp
import cv2
import numpy as np

file_name = "landmark_test.mp4"

cap = cv2.VideoCapture(file_name)

while cap.isOpened():
    ret, frame = cap.read()

    if ret == True:
        cv2.imshow("Frame", frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else: 
        break

cap.release()
cv2.destroyAllWindows()