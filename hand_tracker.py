import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, max_num_hands=2, detection_confidence=0.7, tracking_confidence=0.7, smoothing_factor=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.smoothing_factor = smoothing_factor
        self.last_finger_pos = None

    def get_finger_tip_position(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return None, None

        hand_landmarks = results.multi_hand_landmarks[0]
        h, w, _ = image.shape

        finger_tips_ids = [8, 12, 16, 20, 4]
        finger_positions = []

        for tip_id in finger_tips_ids:
            x = int(hand_landmarks.landmark[tip_id].x * w)
            y = int(hand_landmarks.landmark[tip_id].y * h)
            finger_positions.append((x, y))

        index_finger_tip = finger_positions[0]
        thumb_tip = finger_positions[4]

        if self.last_finger_pos:
            smoothed_x = int(
                self.smoothing_factor * index_finger_tip[0] + (1 - self.smoothing_factor) * self.last_finger_pos[0])
            smoothed_y = int(
                self.smoothing_factor * index_finger_tip[1] + (1 - self.smoothing_factor) * self.last_finger_pos[1])
            smoothed_pos = (smoothed_x, smoothed_y)
        else:
            smoothed_pos = index_finger_tip

        self.last_finger_pos = smoothed_pos

        # Проверка на клик: если указательный и большой пальцы слишком близко
        distance = np.linalg.norm(np.array(index_finger_tip) - np.array(thumb_tip))
        click_detected = distance < 50  # Порог для распознавания клика

        self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return smoothed_pos, click_detected


