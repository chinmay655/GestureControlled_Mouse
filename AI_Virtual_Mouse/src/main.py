import cv2
from hand_tracker import HandTracker
from gesture_control import GestureController
from mouse_controller import MouseController
from utils import draw_fps
import time

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    hand_tracker = HandTracker(max_hands=1, detection_confidence=0.7)
    gesture_controller = GestureController()
    mouse_controller = MouseController(smoothening=7)

    p_time = 0
    while True:
        success, frame = cap.read()
        if not success:
            print('Failed to read from webcam.')
            break
        frame = cv2.flip(frame, 1)
        landmarks = hand_tracker.detect_hands(frame)

        gesture = gesture_controller.recognize_gesture(landmarks, frame)

        mouse_controller.perform_action(gesture, landmarks, frame)

        # draw fps
        p_time = draw_fps(frame, p_time)

        cv2.imshow('AI Virtual Mouse (Enhanced)', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
