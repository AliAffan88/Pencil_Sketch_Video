import cv2
import streamlit as st
import numpy as np
import tempfile
import os
import time

def pencil_sketch(frame):
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    inverted_frame = 255 - grey_frame
    
    blurred = cv2.GaussianBlur(inverted_frame, (21, 21), 0)
    inverted_blurred = 255 - blurred

    pencil_sketch_frame = cv2.divide(grey_frame, inverted_blurred, scale=256.0)
    
    return pencil_sketch_frame

st.title('MAKE ANY VIDEO INTO PENCIL SKETCH')

uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi"])

if "show_video" not in st.session_state:
    st.session_state.show_video = True

if uploaded_file is not None:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())

    video_placeholder = st.empty()
    
    video_capture = cv2.VideoCapture(temp_file.name)
    
    _, frame = video_capture.read()
    height, width, _ = frame.shape
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    video_writer = cv2.VideoWriter(output_file.name, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
    
    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            break  
        
        pencil_sketch_frame = pencil_sketch(frame)
        
        video_writer.write(cv2.cvtColor(pencil_sketch_frame, cv2.COLOR_GRAY2BGR))
        
        if st.session_state.show_video:
            video_placeholder.image(pencil_sketch_frame, channels="GRAY")
        
        time.sleep(0.03)  # Adjust the delay time as needed (e.g., 0.1 seconds)
    
    video_writer.release()
    video_capture.release()
    
    temp_file.close()
    os.unlink(temp_file.name)

    save_as_button = st.button("Save As")
    if save_as_button:
        st.session_state.show_video = False  # Set the boolean variable to False
        with open(output_file.name, 'rb') as f:
            video_bytes = f.read()
        st.download_button(
            label="Click to save processed video",
            data=video_bytes,
            file_name="processed_video.mp4",
            mime="video/mp4",
        )
