import cv2
import streamlit as st
from fer import FER
import numpy as np
from PIL import Image

# Initialize FER detector
detector = FER(mtcnn=False)

# Function to map emotions to emojis
def get_emoji(emotion):
    emojis = {
        "happy": "😊", "sad": "😢", "angry": "😡",
        "surprise": "😲", "neutral": "😐", "fear": "😨",
        "disgust": "🤢"
    }
    return emojis.get(emotion, "😐")

# Streamlit UI
st.title("Real-Time Emotion Detection")
st.write("Upload an image or use your webcam to detect emotions with emoji!")

# Upload image option
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    frame = np.array(image)

    # Ensure frame is 3-channel BGR
    if len(frame.shape) == 2 or frame.shape[2] == 1:
         frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    # Detect emotions
    results = detector.detect_emotions(frame)

    if results:
        for face in results:
            (x, y, w, h) = face["box"]
            emotions = face["emotions"]
            dominant = max(emotions, key=emotions.get)
            emoji_icon = get_emoji(dominant)

            # Draw rectangle and text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{emoji_icon} {dominant}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        st.image(frame, channels="RGB")
    else:
        st.write("No face detected.")

# Webcam option
if st.button("Open Webcam"):
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.detect_emotions(frame)
        for face in results:
            (x, y, w, h) = face["box"]
            emotions = face["emotions"]
            dominant = max(emotions, key=emotions.get)
            emoji_icon = get_emoji(dominant)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{emoji_icon} {dominant}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        stframe.image(frame, channels="BGR")

    cap.release()
