import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1, y1) and (x2, y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis

def main():
    st.title("Push-up Counter App")
    
    push_up_start = 0
    push_up_count = 0

    cap = cv2.VideoCapture(0)  # 0 for default webcam, you can change it to the video file path

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

        while st.checkbox("Capture Video", value=True):
            success, image = cap.read()
            if not success:
                st.warning("Unable to capture video.")
                break

            image_height, image_width, _ = image.shape
            image.flags.writeable = False

            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            nose_point = (int(results.pose_landmarks.landmark[0].x * image_width), 
                          int(results.pose_landmarks.landmark[0].y * image_height))
            
            right_wrist = (int(results.pose_landmarks.landmark[16].x * image_width), 
                           int(results.pose_landmarks.landmark[16].y * image_height))
            
            right_shoulder = (int(results.pose_landmarks.landmark[12].x * image_width), 
                              int(results.pose_landmarks.landmark[12].y * image_height))

            if distanceCalculate(right_shoulder, right_wrist) < 130:
                push_up_start = 1
            elif push_up_start and distanceCalculate(right_shoulder, right_wrist) > 250:
                push_up_count += 1
                push_up_start = 0

            st.image(image, channels="BGR", use_column_width=True)
            st.write("Push-up Count:", push_up_count)

            time.sleep(0.01)

    cap.release()

if __name__ == "__main__":
    main()
