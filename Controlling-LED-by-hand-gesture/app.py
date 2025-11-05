import cv2
import mediapipe as mp
import requests
import time
import threading
import os

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# ========================
# ESP32 Configuration
# ========================
ESP32_IP = "http://10.150.17.152"  # ← Replace with your ESP32 IP
BASE_URL = f"{ESP32_IP}/led"       # Base URL for LED control
r = requests.get(ESP32_IP)
print(r.text)

# ========================
# MediaPipe Hands Setup
# ========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# ========================
# Global Variables
# ========================
last_state = [False, False, False, False, False]
last_send_time = 0
SEND_INTERVAL = 0.3  # Minimum time between commands (seconds)

# ========================
# Function to send LED command asynchronously
# ========================
def send_led_command(endpoint):
    def task():
        try:
            url = f"{BASE_URL}/{endpoint}"
            response = requests.get(url, timeout=2)
            print(f"Sent command: {endpoint}, ESP32 Response: {response.text}")
        except Exception as e:
            print(f"Failed to send command: {endpoint}, Error: {e}")
    threading.Thread(target=task).start()

# ========================
# Function to detect finger states and send commands
# ========================
def count_fingers(hand_landmarks):
    global last_state, last_send_time

    # Finger state detection (up = True, down = False)
    thumb_up = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < \
               hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    index_up = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < \
               hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_up = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < \
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    ring_up = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < \
              hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    pinky_up = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < \
               hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y

    finger_status = [thumb_up, index_up, middle_up, ring_up, pinky_up]
    now = time.time()

    # Send commands only if finger state changed and interval passed
    if finger_status != last_state and (now - last_send_time) > SEND_INTERVAL:
        send_led_command("thumb/on" if thumb_up else "thumb/off")
        send_led_command("index/on" if index_up else "index/off")
        send_led_command("middle/on" if middle_up else "middle/off")
        send_led_command("ring/on" if ring_up else "ring/off")
        send_led_command("pinky/on" if pinky_up else "pinky/off")
        last_state = finger_status.copy()
        last_send_time = now

    return finger_status

# ========================
# Main Loop
# ========================
def main():
    cap = cv2.VideoCapture(0)  # Adjust camera index if needed

    if not cap.isOpened():
        print("Error: Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror the frame
        # Resize for faster processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.resize(frame_rgb, (320, 240))

        # Detect hands
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on original frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # Detect fingers and control LEDs
                count_fingers(hand_landmarks)

        # Display the frame
        cv2.imshow("Hand Gesture Recognition", frame)

        # Exit on 'Esc' key
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ========================
# Entry Point
# ========================
if __name__ == "__main__":
    main()
