import cv2
import numpy as np
import os

INPUT_DIR = "subgrid"
OUTPUT_DIR = "subgrid_clean"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def find_crop_bounds(gray, threshold_ratio=0.85):
    h, w = gray.shape

    _, binary = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    row_density = np.sum(binary > 0, axis=1) / w
    col_density = np.sum(binary > 0, axis=0) / h

    top = 0
    while top < h and row_density[top] > threshold_ratio:
        top += 1

    bottom = h - 1
    while bottom > 0 and row_density[bottom] > threshold_ratio:
        bottom -= 1

    left = 0
    while left < w and col_density[left] > threshold_ratio:
        left += 1

    right = w - 1
    while right > 0 and col_density[right] > threshold_ratio:
        right -= 1

    return top, bottom, left, right


for fname in os.listdir(INPUT_DIR):
    if not fname.endswith(".png"):
        continue

    img = cv2.imread(os.path.join(INPUT_DIR, fname))
    if img is None:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    top, bottom, left, right = find_crop_bounds(gray)

    if bottom - top < 20 or right - left < 20:
        print(f"TOO LESS: {fname}")
        continue

    cropped = img[top:bottom, left:right]

    out_path = os.path.join(OUTPUT_DIR, fname)
    cv2.imwrite(out_path, cropped)

    print(f"CLEANED: {fname}")
