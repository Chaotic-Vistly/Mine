import cv2
import pytesseract
import os
import re
import time
import joblib
import numpy as np
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Load trained model
from sklearn.ensemble import RandomForestClassifier
model = joblib.load("model.pkl")
IMG_SIZE = (32, 32)

# Tesseract config
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

# Output directories
output_dir = "detections"
os.makedirs(output_dir, exist_ok=True)

feedback_file = "feedback_log.csv"
if not os.path.exists(feedback_file):
    with open(feedback_file, "w") as f:
        f.write("number,confidence,label,timestamp\n")

# Globals
pending_feedback = False
last_detected_number = None
last_detection_time = 0
cooldown_seconds = 5
current_number = None
current_confidence = None
last_saved_image = None

# GUI setup
root = tk.Tk()
root.title("Digit Detector (Tesseract + Model)")
root.geometry("1280x600")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

label_camera = ttk.Label(root)
label_camera.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

label_processed = ttk.Label(root)
label_processed.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

label_info = ttk.Label(root, text="🧠 Waiting for number...", font=('Arial', 14))
label_info.grid(row=1, column=0, columnspan=2)

# Entry and button for manual correction
entry_corrected = ttk.Entry(root)
entry_corrected.grid(row=2, column=0, padx=5, pady=5)
btn_submit_correction = ttk.Button(root, text="📤 Submit Correction", command=lambda: submit_manual_correction(entry_corrected.get()))
btn_submit_correction.grid(row=2, column=1, padx=5, pady=5)
entry_corrected.grid_remove()
btn_submit_correction.grid_remove()

# Feedback buttons
btn_correct = ttk.Button(root, text="✅ Correct", command=lambda: save_feedback(True))
btn_correct.grid(row=3, column=0, pady=10)
btn_wrong = ttk.Button(root, text="❌ Wrong", command=lambda: save_feedback(False))
btn_wrong.grid(row=3, column=1, pady=10)

# Sharpen image helper
def sharpen_image(image):
    blur = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.addWeighted(image, 1.5, blur, -0.5, 0)

cap = cv2.VideoCapture(0)

# Predict with fallback model
def predict_with_model(image):
    img_resized = cv2.resize(image, IMG_SIZE)
    img_flat = img_resized.flatten().reshape(1, -1)
    prediction = model.predict(img_flat)[0]
    return str(prediction)

# Prompt feedback question
def show_feedback_prompt():
    label_info.config(text=f"❓ Was {current_number} correct? Use ✅ / ❌")

# Save user feedback and crop
def save_feedback(correct):
    global current_number, current_confidence, last_saved_image, pending_feedback
    if not current_number or last_saved_image is None:
        return
    label = "correct" if correct else "wrong"
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Log feedback
    with open(feedback_file, "a") as f:
        f.write(f"{current_number},{current_confidence},{label},{timestamp}\n")
    # Save crop to dataset
    folder = current_number if correct else 'unlabeled'
    dataset_dir = os.path.join("dataset", folder)
    os.makedirs(dataset_dir, exist_ok=True)
    crop_img = cv2.resize(last_saved_image, (32, 32))
    cv2.imwrite(os.path.join(dataset_dir, f"{timestamp}.png"), crop_img)
    # Show correction entry if wrong
    if not correct:
        entry_corrected.delete(0, tk.END)
        entry_corrected.grid()
        btn_submit_correction.grid()
    else:
        entry_corrected.grid_remove()
        btn_submit_correction.grid_remove()
        pending_feedback = False
    label_info.config(text=f"✅ Feedback saved: {current_number} as {label}")
    current_number = None

# Handle manual correction input
def submit_manual_correction(value):
    global current_number, last_saved_image, pending_feedback
    val = value.strip()
    if not (val.isdigit() or val.lower()=='nothing'):
        label_info.config(text="⚠️ Enter a valid number or 'nothing'")
        return
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    folder = val if val.isdigit() else 'unlabeled'
    dataset_dir = os.path.join("dataset", folder)
    os.makedirs(dataset_dir, exist_ok=True)
    crop_img = cv2.resize(last_saved_image, (32, 32))
    cv2.imwrite(os.path.join(dataset_dir, f"{timestamp}.png"), crop_img)
    with open(feedback_file, "a") as f:
        f.write(f"{val},{current_confidence},manual,{timestamp}\n")
    label_info.config(text=f"📤 Manual correction saved: {val}")
    entry_corrected.grid_remove()
    btn_submit_correction.grid_remove()
    current_number = None
    pending_feedback = False

# Main update loop
def update_frames():
    global last_detected_number, last_detection_time
    global current_number, current_confidence, last_saved_image, pending_feedback

    # Read a frame
    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frames)
        return

    # Preprocess
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    roi = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(roi, 170, 255, cv2.THRESH_BINARY)
    roi_resized = cv2.resize(thresh, None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)

    # If we're waiting on your feedback, don't run detection again
    if pending_feedback:
        root.after(30, update_frames)
        return

    # If the thresholded image is almost blank, skip detection
    if cv2.countNonZero(thresh) < 500:
        label_info.config(text="🧠 No number detected")
        root.after(30, update_frames)
        return

    # 1) Try Tesseract OCR
    data = pytesseract.image_to_data(roi_resized, config=custom_config,
                                     output_type=pytesseract.Output.DICT)
    detected_number = None
    detected_conf = 0
    for i, txt in enumerate(data['text']):
        txt = txt.strip()
        try:
            conf = int(data['conf'][i])
        except:
            conf = 0

        if re.fullmatch(r'\d{1,3}', txt) and conf >= 60:
            detected_number = txt
            detected_conf = conf
            break

    # 2) If OCR found nothing, skip fallback entirely
    if not detected_number:
        label_info.config(text="🧠 No number detected")
    else:
        # 3) On a new detection, save and prompt feedback
        now = time.time()
        if (detected_number != last_detected_number or
            now - last_detection_time > cooldown_seconds):

            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            cv2.imwrite(os.path.join(output_dir, f"detected_{timestamp}.png"), frame)
            last_saved_image = thresh
            last_detected_number = detected_number
            last_detection_time = now
            current_number = detected_number
            current_confidence = detected_conf
            pending_feedback = True
            show_feedback_prompt()

    # Update the UI panels
    cam_img = cv2.resize(frame, (600, 450))
    proc_img = cv2.resize(roi_resized, (600, 450))
    imgtk1 = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(cam_img, cv2.COLOR_BGR2RGB)))
    imgtk2 = ImageTk.PhotoImage(Image.fromarray(proc_img))

    label_camera.config(image=imgtk1)
    label_camera.imgtk = imgtk1
    label_processed.config(image=imgtk2)
    label_processed.imgtk = imgtk2

    root.after(30, update_frames)


update_frames()
root.mainloop()
cap.release()
cv2.destroyAllWindows()
