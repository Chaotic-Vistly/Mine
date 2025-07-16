import cv2
import pytesseract
import os
from datetime import datetime
import re
import time

# Tesseract setup
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

# Output folder
output_dir = "detections"
os.makedirs(output_dir, exist_ok=True)

# Feedback log
feedback_file = "feedback_log.csv"
if not os.path.exists(feedback_file):
    with open(feedback_file, "w") as f:
        f.write("number,confidence,label,timestamp\n")

# Webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not access camera.")
    exit()

print("✅ Video capture started. Press 'q' to quit.")

last_detected_number = None
last_detection_time = 0
cooldown_seconds = 5  # Time before allowing same number again

def sharpen_image(image):
    blur = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.addWeighted(image, 1.5, blur, -0.5, 0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Preprocessing for black digits on white
    roi = sharpen_image(gray)
    roi = cv2.GaussianBlur(roi, (3, 3), 0)
    _, thresh = cv2.threshold(roi, 160, 255, cv2.THRESH_BINARY)  # ✅ no inversion

    # Upscale for OCR
    roi_resized = cv2.resize(thresh, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    # OCR
    data = pytesseract.image_to_data(roi_resized, config=custom_config, output_type=pytesseract.Output.DICT)

    detected_number = None
    detected_confidence = None

    for i, word in enumerate(data['text']):
        conf = int(data['conf'][i])
        word_clean = word.strip()

        if re.fullmatch(r'\d{1,3}', word_clean) and conf >= 60:
            detected_number = word_clean
            detected_confidence = conf
            break

    current_time = time.time()

    if detected_number:
        if detected_number != last_detected_number or (current_time - last_detection_time > cooldown_seconds):
            now = datetime.now()
            timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
            readable_time = now.strftime('%Y-%m-%d %H:%M:%S')
            filename = f"{output_dir}/detected_{timestamp}.png"
            cv2.imwrite(filename, frame)

            print(f"\n🧠 Detected number: {detected_number} (confidence: {detected_confidence}%)")
            print(f"📸 Saved image as: {filename}")
            feedback = input("✅ Is this correct? (y/n): ").strip().lower()
            label = "correct" if feedback == 'y' else "wrong"

            with open(feedback_file, "a") as f:
                f.write(f"{detected_number},{detected_confidence},{label},{timestamp}\n")

            last_detected_number = detected_number
            last_detection_time = current_time

    # Show feed
    cv2.imshow("Camera Feed", frame)
    cv2.imshow("OCR Input (Processed)", roi_resized)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
