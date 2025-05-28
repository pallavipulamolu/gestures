import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize keyboard controller
keyboard = Controller()

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    results = hands.process(image_rgb)

    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of the index finger tip
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger_tip.x * image.shape[1])
            y = int(index_finger_tip.y * image.shape[0])

            # Define regions for control
            if x < image.shape[1] // 3:
                # Left region
                keyboard.press('a')
                keyboard.release('d')
            elif x > 2 * image.shape[1] // 3:
                # Right region
                keyboard.press('d')
                keyboard.release('a')
            else:
                # Center region
                keyboard.release('a')
                keyboard.release('d')

            if y < image.shape[0] // 3:
                # Upper region - accelerate
                keyboard.press('w')
                keyboard.release('s')
            elif y > 2 * image.shape[0] // 3:
                # Lower region - brake
                keyboard.press('s')
                keyboard.release('w')
            else:
                # Middle region
                keyboard.release('w')
                keyboard.release('s')

    else:
        # No hands detected, release all keys
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release('w')
        keyboard.release('s')

    # Display the resulting image
    cv2.imshow('Gesture Controlled Car Racing', image)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
