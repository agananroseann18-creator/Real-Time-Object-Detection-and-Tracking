import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from ultralytics import YOLO
import av
import cv2
from datetime import datetime
import os
import time
import numpy as np

st.set_page_config(page_title="🎥 Live Object Detection & Tracing", layout="centered")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #BBD5DA;
        background-image: radial-gradient(#2d3436 0.5px, transparent 0.5px);
        background-size: 30px 30px;
    }
    h1 {
        color: black;
        text-align: center;
        font-weight: 200;
        letter-spacing: 3px;
        padding: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SAVE_DIR = "detections"
os.makedirs(SAVE_DIR, exist_ok=True)

last_save_time = 0

@st.cache_resource
def load_model():
    model = YOLO("yolov8n.pt")
    return model

model = load_model()

st.title("🎥 Live Object Detection & Tracing ")
st.write("Point your camera at objects to identify them in real-time.")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    alert_target = st.selectbox(
        "🎯 Target Object:",
        ["person", "cell phone", "bottle", "keyboard", "laptop", "mouse"]
    )

with col2:
    conf_threshold = st.slider("🔍 Confidence", 0.1, 1.0, 0.3)

with col3:
    enable_save = st.checkbox("💾 Auto-Save", value=False)

def video_frame_callback(frame):
    global last_save_time

    img = frame.to_ndarray(format="bgr24")

    results = model(img, conf=conf_threshold)

    annotated_frame = results[0].plot()

    boxes = results[0].boxes
    obj_count = len(boxes) if boxes is not None else 0

    cv2.putText(
        annotated_frame,
        f"Objects: {obj_count}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label == alert_target:
                cv2.putText(
                    annotated_frame,
                    f"ALERT: {label.upper()}",
                    (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

                if enable_save:
                    current_time = time.time()
                    if current_time - last_save_time > 2:
                        timestamp = datetime.now().strftime("%H%M%S")
                        filename = os.path.join(
                            SAVE_DIR,
                            f"{label}_{timestamp}.jpg"
                        )
                        cv2.imwrite(filename, annotated_frame)
                        last_save_time = current_time
                break

    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")
webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=video_frame_callback,
    async_processing=True,
    rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
            {"urls": ["stun:stun1.l.google.com:19302"]},
        ]
    },
    media_stream_constraints={
        "video": True,
        "audio": False
    },
)