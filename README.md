# 🎭 Real-Time Face Expression Analyzer

A high-performance, browser-based AI tool designed to detect and categorize human emotions in real-time. Built using **Python**, **DeepFace**, and **Streamlit**, this project features a stabilized HUD and dynamic color-coded feedback.

**🚀 [Live Demo: Face Expression Analyzer](https://face-expression-analyzer.streamlit.app/)**

---

## ✨ Features

* **Real-Time Detection**: Instantly identifies emotions like Happy, Neutral, Sad, Surprise, and Angry.
* **Stabilized Tracking**: Uses **Temporal Smoothing** (Linear Interpolation) to prevent the tracking box from jittering during movement.
* **Cloud-Optimized**: Powered by **WebRTC** for low-latency video streaming directly in the browser.
* **Professional UI**: A custom-styled dark theme designed for a modern user experience.
* **Dynamic HUD**: The interface reacts to your emotions, changing colors instantly to match your "vibe."

---

## 🛠️ Tech Stack

* **Language**: Python 3.13
* **AI Library**: [DeepFace](https://github.com/serengil/deepface) (OpenCV backend)
* **Web Framework**: Streamlit
* **Video Processing**: Streamlit-WebRTC & PyAV
* **Environment**: Cloud-deployed on Streamlit Community Cloud

---

## 🚀 Local Installation

If you want to run this project on your D: drive:

1.  **Clone the Repo**:
    ```bash
    git clone [https://github.com/rishav1328/Face-Expression-Analyzer.git](https://github.com/rishav1328/Face-Expression-Analyzer.git)
    ```
2.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

---

## 👨‍💻 Developer
**Rishav Biswas**
* **Position**: Junior HR Executive at InAmigos Foundation
* **Interests**: Web Development, Python, and AI-driven automation.

---

### 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
