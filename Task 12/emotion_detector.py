import cv2
from fer import FER
import numpy as np
import emoji

# Initialize detector
detector = FER(mtcnn=False)

# Webcam capture
cap = cv2.VideoCapture(0)

def get_emoji(emotion):
    emojis = {
        "happy": "😊", "sad": "😢", "angry": "😡",
        "surprise": "😲", "neutral": "😐", "fear": "😨",
        "disgust": "🤢"
    }
    return emojis.get(emotion, "😐")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect emotions
    results = detector.detect_emotions(frame)

    for face in results:
        (x, y, w, h) = face["box"]
        emotions = face["emotions"]
        dominant = max(emotions, key=emotions.get)
        emoji_icon = get_emoji(dominant)

        # Draw face box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Show emoji + emotion name
        cv2.putText(frame, f"{emoji_icon} {dominant}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        # Draw probability bars
        bar_x = x
        bar_y = y + h + 20
        for emotion, score in emotions.items():
            cv2.putText(frame, f"{emotion}:", (bar_x, bar_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.rectangle(frame, (bar_x+80, bar_y-10),
                          (bar_x+int(200*score), bar_y+10),
                          (0, 255, 255), -1)
            bar_y += 25

    cv2.imshow("Advanced Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
