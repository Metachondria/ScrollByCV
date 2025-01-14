import cv2
from hand_tracker import HandTracker
from overlay import Overlay
import pyautogui
import numpy as np

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

    # Для отслеживания предыдущей вертикальной позиции пальца и скорости прокрутки
    last_y_position = None
    last_scroll_time = 0  # Время последней прокрутки
    scroll_sensitivity = 10  # Чувствительность прокрутки (больше значение = более чувствительная прокрутка)
    scroll_speed = 100  # Степень прокрутки (больше значение = более быстрая прокрутка)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось получить кадр")
            break

        frame = cv2.flip(frame, 1)

        finger_point, _ = hand_tracker.get_finger_tip_position(frame)

        if finger_point:
            cv2.circle(frame, finger_point, 10, (0, 0, 255), -1)
        if finger_point:
            frame_height, frame_width, _ = frame.shape
            screen_coords = map_finger_to_screen(finger_point, frame_width, frame_height, screen_width, screen_height)
            if screen_coords:
                screen_x, screen_y = screen_coords
                overlay.update_position(screen_x, screen_y)

                if last_y_position is not None:
                    delta_y = finger_point[1] - last_y_position

                    if abs(delta_y) > scroll_sensitivity:
                        # NEED FIX
                        if delta_y < 0:
                            pyautogui.scroll(-110)  # SCROLL DOWN
                        # elif delta_y > 0:
                        #     pyautogui.scroll(0)  # Прокрутка вниз

                last_y_position = finger_point[1]

        cv2.imshow('Finger Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
