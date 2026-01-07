import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import webbrowser

# -------------------- LOAD ENV --------------------
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# -------------------- SPOTIFY --------------------
spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
)

# -------------------- LOAD MODEL --------------------
model = load_model("model.h5")
labels = np.load("labels.npy")

# -------------------- MEDIAPIPE --------------------
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

# -------------------- SPOTIFY SEARCH --------------------
def recommend_music(mood):
    queries = [
        f"{mood} Telugu song",
        f"{mood} English song"
    ]

    results = []
    for q in queries:
        data = spotify.search(q=q, type="track", limit=5)
        for item in data["tracks"]["items"]:
            results.append(item["external_urls"]["spotify"])

    return results

# -------------------- CAMERA --------------------
cap = cv2.VideoCapture(0)
emotion_detected = None
frame_count = 0

print("🎥 Camera started... Detecting emotion")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = holistic.process(rgb)

    landmarks = []

    if res.face_landmarks:
        for lm in res.face_landmarks.landmark:
            landmarks.append(lm.x)
            landmarks.append(lm.y)

        landmarks = np.array(landmarks).reshape(1, -1)

        pred = model.predict(landmarks, verbose=0)
        emotion = labels[np.argmax(pred)]

        frame_count += 1

        cv2.putText(
            frame,
            f"Mood: {emotion}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Confirm emotion after stable frames
        if frame_count > 30:
            emotion_detected = emotion
            break

    cv2.imshow("Live Mood Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# -------------------- MUSIC --------------------
if emotion_detected:
    print(f"🎯 Detected Mood: {emotion_detected}")
    songs = recommend_music(emotion_detected)

    print("🎶 Opening Spotify songs...")
    for url in songs[:2]:
        webbrowser.open(url)
else:
    print("❌ Mood not detected")
