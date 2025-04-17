import cv2
import mediapipe as mp
import sympy as sp
import tkinter as tk
from tkinter import messagebox
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

x, y, n = sp.symbols('x y n')  # Define symbolic variables

LANDMARKS_5_TO_17 = [
    mp_hands.HandLandmark.INDEX_FINGER_MCP,
    mp_hands.HandLandmark.INDEX_FINGER_PIP,
    mp_hands.HandLandmark.INDEX_FINGER_DIP,
    mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
    mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
    mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
    mp_hands.HandLandmark.RING_FINGER_MCP,
    mp_hands.HandLandmark.RING_FINGER_PIP,
    mp_hands.HandLandmark.RING_FINGER_DIP,
    mp_hands.HandLandmark.PINKY_MCP,
]

detected_numbers = ""
last_update_time = time.time()

def check_thumb_in_range(hand_landmarks):
    thumb_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    
    for lm in LANDMARKS_5_TO_17:
        lm_x = hand_landmarks.landmark[lm].x
        lm_y = hand_landmarks.landmark[lm].y
        if abs(thumb_tip_x - lm_x) < 0.05 and abs(thumb_tip_y - lm_y) < 0.05:
            return True
    return False

def map_gesture_to_symbol(hand_landmarks, handedness):
    thumb_extended = check_finger_extended(hand_landmarks, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.THUMB_IP)
    thumb_in_range = check_thumb_in_range(hand_landmarks)
    index_extended = check_finger_extended(hand_landmarks, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_DIP)
    middle_extended = check_finger_extended(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP)
    ring_extended = check_finger_extended(hand_landmarks, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_DIP)
    pinky_extended = check_finger_extended(hand_landmarks, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_DIP)

    finger_count = sum([index_extended, middle_extended, ring_extended, pinky_extended])

    if handedness == "Left":
        # Right Hand: Basic operations and numbers
        if ring_extended and pinky_extended and not index_extended and not middle_extended:
            return '+'
        if ring_extended and pinky_extended and middle_extended and not index_extended and thumb_in_range:
            return '-'
        elif not middle_extended and ring_extended and pinky_extended and index_extended:
            return '*'
        elif middle_extended and not ring_extended and pinky_extended and index_extended:
            return '/'
        elif pinky_extended and not ring_extended and not index_extended and not middle_extended:
            return "SHOW_RESULT"
        
        if thumb_in_range and finger_count == 1 and index_extended:
            return "1"
        elif thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "6"
        elif thumb_in_range and finger_count == 2 and index_extended and middle_extended:
            return "2"
        elif thumb_in_range and finger_count == 3 and index_extended and middle_extended and ring_extended:
            return "3"
        elif index_extended and pinky_extended and not thumb_in_range:
            return "5"
        elif finger_count == 1 and index_extended and not thumb_in_range:
            return "7"
        elif finger_count == 2 and index_extended and middle_extended:
            return "8"
        elif finger_count == 2 and index_extended and pinky_extended and not middle_extended and not ring_extended:
            return "0"
        elif finger_count == 3 and not thumb_in_range and not index_extended and pinky_extended and middle_extended and ring_extended:
            return "9"
        elif finger_count == 4 and index_extended and middle_extended and ring_extended and pinky_extended:
            return "4"
        elif finger_count == 5 and not thumb_in_range:
            return "5"
        else:
            return "Unknown gesture"
        
    elif handedness == "Right":
        # Left Hand: Advanced operations and variables
        if index_extended and thumb_in_range and middle_extended and not ring_extended and not pinky_extended:
            return '^'  # Power operation
        elif index_extended and thumb_in_range and not middle_extended and not ring_extended and not pinky_extended:
            return 'x'  # Variable x
        elif thumb_in_range and finger_count == 3 and index_extended and middle_extended and ring_extended:
            return "y"  # Variable y
        elif thumb_extended and not thumb_in_range and index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return 'd/dx'  # Derivation
        elif thumb_extended and not thumb_in_range and middle_extended and not index_extended and not ring_extended and not pinky_extended:
            return '∫'  # Integration
        elif thumb_extended and index_extended and middle_extended and not ring_extended and not pinky_extended:
            return 'Σ'  # Summation
        elif pinky_extended and not ring_extended and not index_extended and not middle_extended:
            return '('  # Open parenthesis
        elif not thumb_in_range and not pinky_extended and not index_extended and not middle_extended and not ring_extended:
            return ')'  # Close parenthesis
        elif pinky_extended and ring_extended and middle_extended and index_extended and not thumb_in_range:
            return "backspace"
        else:
            return "Unknown gesture"

def check_finger_extended(hand_landmarks, tip, dip):
    return hand_landmarks.landmark[tip].y < hand_landmarks.landmark[dip].y

def solve_equation(expression):
    try:
        if 'd/dx' in expression:
            # Handle derivation
            expr = expression.replace('d/dx', '')
            result = sp.diff(sp.sympify(expr), x)
        elif '∫' in expression:
            # Handle integration
            expr = expression.replace('∫', '')
            result = sp.integrate(sp.sympify(expr), x)
        elif 'Σ' in expression:
            # Handle summation
            expr = expression.replace('Σ', '')
            result = sp.Sum(sp.sympify(expr), (n, 1, 10)).doit()  # Sum from n=1 to 10
        else:
            # Handle basic expressions
            result = sp.sympify(expression)
            result = sp.simplify(result)
    except sp.SympifyError:
        return "Invalid Expression"
    return result

def show_solution(equation):
    equation=equation.replace("int ",'∫')
    equation=equation.replace("sigma ",'Σ')
    result = solve_equation(equation)
    messagebox.showinfo("Solution", f"The result is: {result}")

root = tk.Tk()
root.title("Virtual Calculator")

cap = cv2.VideoCapture(0)

def video_stream():
    global detected_numbers, last_update_time

    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            handedness = handedness.classification[0].label  # Get handedness (Left or Right)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            symbol = map_gesture_to_symbol(hand_landmarks, handedness)
            print(f"Detected symbol ({handedness} hand):", symbol)

            current_time = time.time()
            if current_time - last_update_time > 3:
                if symbol != "Unknown gesture" and symbol != "SHOW_RESULT" and symbol != "backspace":
                    if symbol=='∫':
                        detected_numbers += "int "
                    elif symbol=='Σ':
                        detected_numbers += "sigma "
                    else:
                        detected_numbers += symbol
                if symbol=="backspace" and detected_numbers:
                    detected_numbers = detected_numbers[:-1]
                elif symbol == "SHOW_RESULT":
                    show_solution(detected_numbers)
                    detected_numbers = ""
                last_update_time = current_time

    cv2.putText(frame, detected_numbers, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Hand Gesture Detection", frame)
    root.after(10, video_stream)

btn = tk.Button(root, text="Show Solution", command=lambda: show_solution(detected_numbers))
btn.pack(pady=20)

root.after(10, video_stream)
root.mainloop()

cap.release()
cv2.destroyAllWindows()
