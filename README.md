# 🔒 Hand Gesture Lock 

This project leverages **MediaPipe** for hand-tracking to enable **gesture-based encryption and decryption** of folders. It uses **Fernet encryption** from the `cryptography` library, with the encryption key securely stored in an environment variable (`lockdf`). Three distinct hand gestures are used to lock (encrypt) and unlock (decrypt) a folder, making the security mechanism both intuitive and innovative.

## 🛠 Features

- **Gesture Detection:** Uses **MediaPipe Hand** to detect three unique hand gestures.
- **Fernet Encryption:** Encrypts all contents of a folder securely using **AES-128 encryption**.
- **Environment Variable for Security:** The encryption key is stored in the environment variable `lockdf`.
- **Bidirectional Operations:** Supports **encryption and decryption** using gestures.
- **Seamless Integration:** Works with **Python** and **MediaPipe** to create a smooth user experience.

---

## 🧰 Requirements

Make sure you have the following installed:  

- Python 3.x  
- MediaPipe  
- Cryptography library  

## 💡 How It Works

Gesture Recognition:

- The webcam captures hand movements.
- MediaPipe processes the input to detect predefined gestures.
- Encryption/Decryption based on user input

When the 3 recognized gestures are performed in order, the Fernet key from the environment variable (lockdf) is used to encrypt or decrypt the folder.
All files within the folder are restored to their original form.
