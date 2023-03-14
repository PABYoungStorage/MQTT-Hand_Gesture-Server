import mediapipe as mp
import cv2
import numpy as np
import requests

# Connect to the video server
url = 'http://192.168.1.10:8000/get_frame'
response = requests.get(url, stream=True)

# Initialize the MediaPipe hand detection model
mp_hands = mp.solutions.hands.Hands()

# Process the video frames
for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        # Read the video frame
        frame = cv2.imdecode(np.frombuffer(chunk, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Convert the frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame using the MediaPipe hand detection model
        results = mp_hands.process(frame)

        # Extract hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Do something with the hand landmarks
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])

        # Display the recognized gesture
        cv2.imshow('Hand Gesture Recognition', frame)

        # Exit on ESC key press
        if cv2.waitKey(1) == 27:
            break

# Release the video capture and destroy all windows
response.close()
mp_hands.close()
cv2.destroyAllWindows()
