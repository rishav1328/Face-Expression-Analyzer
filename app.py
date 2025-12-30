import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import cv2
import numpy as np
from deepface import DeepFace
import av

# --- 1. UI CONFIG & STYLING ---
st.set_page_config(page_title="Rishav's Expression Analyzer", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .title-text {
        font-family: 'Segoe UI', sans-serif;
        color: #FFFFFF;
        text-align: center;
        text-shadow: 0 0 15px #00f2ff;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>⚡ EXPRESSION ANALYSIS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>CONNECT ON LINKEDIN | DEV: RISHAV</p>", unsafe_allow_html=True)

# --- 2. GLOBAL SETTINGS ---
COLOR_MAP = {
    "happy": (0, 255, 0),      # Green
    "sad": (255, 0, 0),        # Blue (OpenCV uses BGR)
    "angry": (0, 0, 255),      # Red
    "surprise": (0, 255, 255), # Yellow
    "neutral": (255, 255, 255) # White
}

# --- 3. THE "BRAIN" (VIDEO PROCESSOR) ---
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.last_pos = None
        self.smooth_factor = 0.3
        self.frame_count = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1

        # Only analyze every 3rd frame to stop cloud lag
        if self.frame_count % 3 == 0:
            try:
                # Optimized backend for high FPS
                results = DeepFace.analyze(img, actions=['emotion'], 
                                         detector_backend='opencv', 
                                         enforce_detection=False, silent=True)
                res = results[0]
                vibe = res['dominant_emotion']
                color = COLOR_MAP.get(vibe, (255, 255, 255))
                
                # Target coordinates
                tx, ty, tw, th = res['region']['x'], res['region']['y'], res['region']['w'], res['region']['h']
                
                # Temporal Smoothing Logic
                if self.last_pos is None:
                    self.last_pos = [tx, ty, tw, th]
                
                lx, ly, lw, lh = self.last_pos
                nx = int(lx + (tx - lx) * self.smooth_factor)
                ny = int(ly + (ty - ly) * self.smooth_factor)
                nw = int(lw + (tw - lw) * self.smooth_factor)
                nh = int(lh + (th - lh) * self.smooth_factor)
                self.last_pos = [nx, ny, nw, nh]

                # Draw the Stabilized HUD
                cv2.rectangle(img, (nx, ny), (nx+nw, ny+nh), color, 3)
                cv2.rectangle(img, (nx, ny-45), (nx+nw, ny), (0, 0, 0), -1)
                cv2.putText(img, vibe.upper(), (nx+10, ny-12), 
                            cv2.FONT_HERSHEY_DUPLEX, 1.0, color, 2)
            except:
                pass

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 4. LAUNCHER ---
webrtc_streamer(
    key="expression-analysis",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessor,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)