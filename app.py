import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import cv2
import numpy as np
from deepface import DeepFace
import av

# --- UI STYLING ---
st.set_page_config(page_title="Rishav's Expression Analyzer", layout="wide")
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⚡ EXPRESSION ANALYSIS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>STABILIZED HUD | DEV: RISHAV</p>", unsafe_allow_html=True)

COLOR_MAP = {
    "happy": (0, 255, 0), "sad": (255, 0, 0), "angry": (0, 0, 255),
    "surprise": (0, 255, 255), "neutral": (255, 255, 255)
}

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.last_pos = None
        # LOWER FACTOR = MORE STABLE (0.1 to 0.15 is the sweet spot for jitter)
        self.smooth_factor = 0.15 
        self.frame_count = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame_count += 1

        # Skip frames to keep FPS high
        if self.frame_count % 3 == 0:
            try:
                results = DeepFace.analyze(img, actions=['emotion'], 
                                         detector_backend='opencv', 
                                         enforce_detection=False, silent=True)
                res = results[0]
                vibe = res['dominant_emotion']
                color = COLOR_MAP.get(vibe, (255, 255, 255))
                
                # New coordinates from the detector
                tx, ty, tw, th = res['region']['x'], res['region']['y'], res['region']['w'], res['region']['h']
                
                # ENHANCED SMOOTHING: Box moves only 15% toward the new spot per frame
                if self.last_pos is None:
                    self.last_pos = [tx, ty, tw, th]
                
                lx, ly, lw, lh = self.last_pos
                nx = int(lx + (tx - lx) * self.smooth_factor)
                ny = int(ly + (ty - ly) * self.smooth_factor)
                nw = int(lw + (tw - lw) * self.smooth_factor)
                nh = int(lh + (th - lh) * self.smooth_factor)
                self.last_pos = [nx, ny, nw, nh]

                # Draw the smooth box
                cv2.rectangle(img, (nx, ny), (nx+nw, ny+nh), color, 3)
                cv2.rectangle(img, (nx, ny-45), (nx+nw, ny), (0, 0, 0), -1)
                cv2.putText(img, vibe.upper(), (nx+10, ny-12), 
                            cv2.FONT_HERSHEY_DUPLEX, 1.0, color, 2)
            except:
                pass

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="stabilized-analysis",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessor,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)