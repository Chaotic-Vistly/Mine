import os
import cv2
import pytesseract
import pandas as pd
from datetime import datetime

# Paths
detections_dir = "detections"
dataset_dir = "dataset"
log_path = "feedback_log.csv"

# Ensure dataset folder exists
os.makedirs(dataset_dir, exist_ok=True)

# Load feedback
df = pd.read_csv(log_path)

# Use only "correct" detections
df = df[df['label'] == 'correct']

# Tesseract config
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

count = 0
for _, row in df.iterrows():
    label = str(row['number'])
    timestamp = row['timestamp']
    filename = f"detected_{timestamp}.png"
    image_path = os.path.join(detections_dir, filename)

    if not os.path.exists(image_path):
        continue

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # OCR + bounding box
    data = pytesseract.image_to_data(gray, config=custom_config, output_type=pytesseract.Output.DICT)
    for i, text in enumerate(data['text']):
        word = text.strip()
        try:
            conf = int(data['conf'][i])
        except:
            conf = 0

        if word == label and conf >= 60:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            crop = gray[y:y+h, x:x+w]
            save_folder = os.path.join(dataset_dir, label)
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, f"{timestamp}_{count}.png")
            cv2.imwrite(save_path, crop)
            count += 1
            break

print(f"\n✅ Saved {count} cropped digit images to 'dataset/'")
