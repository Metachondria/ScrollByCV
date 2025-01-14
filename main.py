# main.py

import cv2
from hand_tracker import HandTracker
from overlay import Overlay
import pyautogui

def map_finger_to_screen(finger_point, frame_width, frame_height, screen_width, screen_height):
    if finger_point is None:
        return None
    x, y = finger_point
    screen_x = (x / frame_width) * screen_width
    screen_y = (y / frame_height) * screen_height
    return screen_x, screen_y

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось открыть веб-камеру")
        return

    hand_tracker = HandTracker(max_num_hands=1)
    overlay = Overlay()
    overlay.start()

    screen_width, screen_height = pyautogui.size()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр")
            break

        frame = cv2.flip(frame, 1)

        finger_point = hand_tracker.get_finger_tip_position(frame)

        if finger_point:
            cv2.circle(frame, finger_point, 10, (0, 0, 255), -1)

        cv2.imshow('Finger Tracking', frame)

        #code for displaying a point on the screen
        if finger_point:
            frame_height, frame_width, _ = frame.shape
            screen_coords = map_finger_to_screen(finger_point, frame_width, frame_height, screen_width, screen_height)
            if screen_coords:
                screen_x, screen_y = screen_coords
                overlay.update_position(screen_x, screen_y)

        # exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
