import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import cv2
import numpy as np

def distance_calculate(p1, p2):
    """p1 and p2 in format (x1, y1) and (x2, y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis

def push_up_count_logic(nose, right_wrist, right_shoulder):
    if distance_calculate(right_shoulder, right_wrist) < 130:
        return 1
    elif push_up_start and distance_calculate(right_shoulder, right_wrist) > 250:
        return 0
    else:
        return 0

def main():
    st.title("Push-up Counter using Streamlit and webrtc-streamer")

    webrtc_ctx = webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDRECV,
        audio=False,
        video_transformer_factory=None,
        async_processing=True,
    )

    if not webrtc_ctx.state.playing:
        return

    push_up_start = 0
    push_up_count = 0

    while True:
        if webrtc_ctx.video_receiver:
            frame = webrtc_ctx.video_receiver.recv()
            image = frame.to_ndarray(format="bgr24")

            # Dummy values for demonstration
            nose = (100, 100)
            right_wrist = (200, 200)
            right_shoulder = (150, 150)

            push_up_count += push_up_count_logic(nose, right_wrist, right_shoulder)

            # Display the push-up count on the video frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (50, 100)
            font_scale = 1
            color = (255, 0, 0)
            thickness = 2
            image = cv2.putText(
                image,
                f"Push-up count: {push_up_count}",
                org,
                font,
                font_scale,
                color,
                thickness,
                cv2.LINE_AA,
            )

            # Show the video frame with push-up count
            st.image(image, channels="BGR", use_column_width=True)

if __name__ == "__main__":
    main()
