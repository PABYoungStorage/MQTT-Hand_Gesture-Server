import cv2
import mediapipe as mp

# Define the hand gesture recognition function
def recognize_gesture(hand_landmarks):
    # Get the coordinates of the thumb and index finger
    thumb_x, thumb_y = hand_landmarks[4][1], hand_landmarks[4][2]
    index_x, index_y = hand_landmarks[8][1], hand_landmarks[8][2]

    # Calculate the distance between the thumb and index finger
    distance = ((thumb_x - index_x)**2 + (thumb_y - index_y)**2)**0.5

    # If the distance is less than a threshold, recognize it as a "fist" gesture
    if distance < 50:
        return "fist"

    # If the distance is greater than a threshold, recognize it as a "palm" gesture
    elif distance > 150:
        return "palm"

    # Otherwise, recognize it as a "pinch" gesture
    else:
        return "pinch"

# Initialize the Mediapipe hand detection module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open a video capture device (here, we use the default webcam)
cap = cv2.VideoCapture("http://192.168.1.10:8000/video_feed")

# Loop through each frame of the video capture
while cap.isOpened():
    # Read the current frame from the video capture
    success, image = cap.read()
    if not success:
        break

    # Convert the image to RGB format and flip it horizontally
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)

    # Run the hand detection module to detect hand landmarks
    results = hands.process(image)

    # If hands are detected, recognize the hand gesture and display the result on the image
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #gesture = recognize_gesture(hand_landmarks.landmark)
            cv2.putText(image, "hand", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the image with the recognized hand gesture
    cv2.imshow("Hand Gesture Recognition", image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()
