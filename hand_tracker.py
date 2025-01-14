import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=2, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def get_finger_tip_position(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return None

        hand_landmarks = results.multi_hand_landmarks[0]
        h, w, _ = image.shape

        # Координаты кончиков пальцев (указательный, средний, безымянный, мизинец, большой палец)
        finger_tips_ids = [8, 12, 16, 20, 4]  # Индексы кончиков пальцев в MediaPipe

        finger_positions = []

        for tip_id in finger_tips_ids:
            x = int(hand_landmarks.landmark[tip_id].x * w)
            y = int(hand_landmarks.landmark[tip_id].y * h)
            finger_positions.append((x, y))


        index_finger_tip = finger_positions[0]

        # Рисуем точки для визуализации (опционально)
        self.mp_draw.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return index_finger_tip
