import os
import cv2
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Paths
DATASET_DIR = 'dataset'
MODEL_PATH = 'model.pkl'
IMG_SIZE = (32, 32)  # Resize all digits to 32x32 for consistency

X = []  # Images
y = []  # Labels

# Load dataset
for label in os.listdir(DATASET_DIR):
    label_path = os.path.join(DATASET_DIR, label)
    if not os.path.isdir(label_path):
        continue
    for filename in os.listdir(label_path):
        file_path = os.path.join(label_path, filename)
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img_resized = cv2.resize(img, IMG_SIZE).flatten()  # Flatten image to 1D
        X.append(img_resized)
        y.append(int(label))

X = np.array(X)
y = np.array(y)

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, MODEL_PATH)
print(f"\n✅ Model trained and saved as '{MODEL_PATH}'")
