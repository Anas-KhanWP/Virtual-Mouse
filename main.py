import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

index_y = 0
thumb_y = 0
click_and_hold_timer = None

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    print('outside', abs(index_y - thumb_y))

                    #the time module to measure the duration when the condition abs(index_y - thumb_y) < 20 is satisfied. If the duration is greater than 1 second, it triggers the "Click & hold" action using pyautogui.mouseDown(). If the condition is not satisfied, it releases the mouse button using pyautogui.mouseUp().
                    if abs(index_y - thumb_y) < 20:
                        if click_and_hold_timer is None:
                            click_and_hold_timer = time.time()
                        elif time.time() - click_and_hold_timer > 1:
                            pyautogui.mouseDown()
                    else:
                        if click_and_hold_timer is not None:
                            pyautogui.mouseUp()
                            click_and_hold_timer = None
                    if abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
