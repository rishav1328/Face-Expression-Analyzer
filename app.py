import streamlit as st
import cv2
from deepface import DeepFace
import numpy as np

st.set_page_config(page_title="Rishav's Vibe System", layout="wide")

# --- 1. SMOOTHING CACHE ---
# This keeps track of the last few positions to "average" them out
if 'last_pos' not in st.session_state:
    st.session_state.last_pos = None

# UI Headers
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⚡ EXPRESSION ANALYSIS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>CONNECT ON LINKEDIN | DEV: RISHAV</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    FRAME_WINDOW = st.image([])

COLOR_MAP = {
    "happy": (0, 255, 0), "sad": (255, 0, 0), "angry": (0, 0, 255),
    "surprise": (0, 255, 255), "neutral": (255, 255, 255)
}

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Stability factor (0.1 = very slow/smooth, 0.9 = fast/jittery)
SMOOTH_FACTOR = 0.3

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    try:
        # Use 'opencv' for speed, but stabilize the results
        results = DeepFace.analyze(frame, actions=['emotion'], 
                                 detector_backend='opencv', 
                                 enforce_detection=False, silent=True)
        res = results[0]
        vibe = res['dominant_emotion']
        color = COLOR_MAP.get(vibe, (255, 255, 255))
        
        # Target coordinates from AI
        tx, ty, tw, th = res['region']['x'], res['region']['y'], res['region']['w'], res['region']['h']
        
        # Apply smoothing math: (New Pos * Factor) + (Old Pos * (1 - Factor))
        if st.session_state.last_pos is None:
            st.session_state.last_pos = [tx, ty, tw, th]
        
        lx, ly, lw, lh = st.session_state.last_pos
        nx = int(lx + (tx - lx) * SMOOTH_FACTOR)
        ny = int(ly + (ty - ly) * SMOOTH_FACTOR)
        nw = int(lw + (tw - lw) * SMOOTH_FACTOR)
        nh = int(lh + (th - lh) * SMOOTH_FACTOR)
        
        st.session_state.last_pos = [nx, ny, nw, nh]

        # Draw Stabilized UI
        cv2.rectangle(frame, (nx, ny), (nx+nw, ny+nh), color, 3)
        cv2.rectangle(frame, (nx, ny-40), (nx+nw, ny), (0, 0, 0), -1)
        cv2.putText(frame, vibe.upper(), (nx+10, ny-12), cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2)
        
    except:
        pass

    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_container_width=True)