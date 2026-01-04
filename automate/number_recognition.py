import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# =============================
# CONFIG
# =============================
CELL_DIR = "cells"
MODEL_PATH = "number_recognition.h5"
IMG_SIZE = 28

EMPTY_RATIO_THRESHOLD = 0.01
CONFIDENCE_THRESHOLD = 0.65   # EMNIST üçün ideal

# =============================
# LOAD MODEL
# =============================
model = load_model(MODEL_PATH)
NUM_CLASSES = model.output_shape[-1]
print(f"✅ Model yükləndi | classes = {NUM_CLASSES}")

# =============================
# EMPTY CHECK
# =============================
def is_empty(cell_gray):
    _, binary = cv2.threshold(
        cell_gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    ratio = cv2.countNonZero(binary) / (binary.shape[0] * binary.shape[1])
    return ratio < EMPTY_RATIO_THRESHOLD

# =============================
# PREPROCESS (EMNIST FINAL FIX)
# =============================
def preprocess(cell_gray):
    # 1. Binary
    _, binary = cv2.threshold(
        cell_gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # 2. Stroke qalınlaşdır (MNIST/EMNIST-ə oxşat)
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)

    # 3. 🔥 EMNIST ORIENTATION FIX (ƏSAS MƏSƏLƏ)
    binary = np.rot90(binary, k=1)
    binary = np.fliplr(binary)

    # 4. Kontur tap → mərkəzləşdirmə
    cnts, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        c = max(cnts, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        digit = binary[y:y+h, x:x+w]
    else:
        digit = binary

    # 5. Kvadrat canvas
    size = max(digit.shape)
    canvas = np.zeros((size, size), dtype=np.uint8)

    y_off = (size - digit.shape[0]) // 2
    x_off = (size - digit.shape[1]) // 2
    canvas[y_off:y_off+digit.shape[0], x_off:x_off+digit.shape[1]] = digit

    # 6. Resize → 28×28
    resized = cv2.resize(canvas, (IMG_SIZE, IMG_SIZE))

    # 7. Normalize
    x = resized.astype("float32") / 255.0
    return x.reshape(1, IMG_SIZE, IMG_SIZE, 1)

# =============================
# PREDICT DIGIT
# =============================
def predict_digit(cell_gray):
    x = preprocess(cell_gray)
    probs = model.predict(x, verbose=0)[0]

    cls = int(np.argmax(probs))
    conf = probs[cls]

    if conf < CONFIDENCE_THRESHOLD:
        return 0

    return cls  # 0–9

# =============================
# BUILD SUDOKU GRID
# =============================
grid = [[0 for _ in range(9)] for _ in range(9)]

for fname in os.listdir(CELL_DIR):
    if not fname.endswith(".png"):
        continue

    # subgrid_2_1_cell_0_2.png
    parts = fname.replace(".png", "").split("_")
    sg_r, sg_c, c_r, c_c = map(int, [parts[1], parts[2], parts[4], parts[5]])

    row = sg_r * 3 + c_r
    col = sg_c * 3 + c_c

    cell = cv2.imread(os.path.join(CELL_DIR, fname), cv2.IMREAD_GRAYSCALE)
    if cell is None:
        continue

    if is_empty(cell):
        grid[row][col] = 0
    else:
        grid[row][col] = predict_digit(cell)

# =============================
# RESULT
# =============================
print("\n🧩 Detected Sudoku Grid:\n")
for r in grid:
    print(r)
