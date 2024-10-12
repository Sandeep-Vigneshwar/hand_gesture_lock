import mediapipe as mp
from time import sleep
import cv2
import os
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()
def save_key(key, filename):
    with open(filename, 'wb') as key_file:
        key_file.write(key)
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
def encrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
def decrypt_folder(folder_path, key):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)
folder_path = "confidential"
key = os.getenv("lockdf")
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

lock_1,lock_2,lock_3 = [1,1,1]
warn_buf=1

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            wrist = landmarks[mp_hands.HandLandmark.WRIST]
            thumb_finger_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
            index_finger_mcp = landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_finger_mcp = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_finger_mcp = landmarks[mp_hands.HandLandmark.RING_FINGER_MCP]
            pinky_mcp = landmarks[mp_hands.HandLandmark.PINKY_MCP]
            index_finger_dip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_DIP]
            middle_finger_dip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
            ring_finger_dip = landmarks[mp_hands.HandLandmark.RING_FINGER_DIP]
            pinky_dip = landmarks[mp_hands.HandLandmark.PINKY_DIP]
            index_finger_pip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            middle_finger_pip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            ring_finger_pip = landmarks[mp_hands.HandLandmark.RING_FINGER_PIP]
            pinky_pip = landmarks[mp_hands.HandLandmark.PINKY_PIP]

            if lock_1==1:
                if index_finger_tip.y<index_finger_dip.y and index_finger_dip.y<index_finger_pip.y and pinky_tip.y<pinky_dip.y and pinky_dip.y<pinky_pip.y and middle_finger_tip.y>middle_finger_mcp.y and ring_finger_tip.y>ring_finger_mcp.y and thumb_finger_tip.x>index_finger_tip.x and thumb_finger_tip.x<pinky_tip.x:
                    lock_1 = 0
                    print("symbol 1 accepted ====> lock 1 released")
                    sleep(0.5)
                    print("waiting for key 2 input =====> ",end="")
            else:
                if lock_2==1:
                    if (thumb_finger_tip.y < index_finger_mcp.y and index_finger_mcp.y < middle_finger_mcp.y and middle_finger_mcp.y<ring_finger_mcp.y and ring_finger_mcp.y<pinky_mcp.y):
                        lock_2 = 0
                        print("symbol 2 accepted ====> lock 2 released")
                        sleep(0.5)
                        print("waiting for key 3 input =====> ", end="")
                else:
                    if lock_3==1:
                        if thumb_finger_tip.x<index_finger_mcp.x and index_finger_tip.y<index_finger_dip.y and index_finger_dip.y<index_finger_pip.y and index_finger_pip.y<index_finger_mcp.y and middle_finger_tip.y<middle_finger_dip.y and middle_finger_dip.y<middle_finger_pip.y and middle_finger_pip.y<middle_finger_mcp.y and thumb_finger_tip.y>index_finger_mcp.y and ring_finger_tip.y>ring_finger_dip.y and pinky_tip.y>pinky_dip.y:
                            lock_3 = 0
                            print("symbol 3 accepted ====> lock 3 released")
        if warn_buf == 1:
            sleep(0.5)
            print("\n\n<======== Lock System ========>\n\nwaiting for key 1 input =====> ", end="")
        warn_buf = 0
    cv2.imshow('lock_system', frame)

    if (cv2.waitKey(10) & 0xFF == ord('q')) or (lock_1==0 and lock_2==0 and lock_3==0):
        break
cap.release()
cv2.destroyAllWindows()
if(lock_1==0 and lock_2==0 and lock_3==0):
    sleep(0.5)
    print("\nALL LOCKS RELEASED =====================> ACCESS GRANTED")
    while True:
        comm = input("encrypt/decrypt : ")
        if comm=="encrypt":
            encrypt_folder(folder_path, key)
            print("Folder encrypted.")
            break
        elif comm=="decrypt":
            decrypt_folder(folder_path, key)
            print("Folder decrypted.")
            break
        elif comm=="cancel":
            break