import cv2
import os

SRC = "cells_raw"   
DST = "cells"       
os.makedirs(DST, exist_ok=True)

for fname in os.listdir(SRC):
    if not fname.lower().endswith(".png"):
        continue

    src_path = os.path.join(SRC, fname)
    dst_path = os.path.join(DST, fname)

    img = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"something went wrong: {fname}")
        continue

    _, bin_img = cv2.threshold(
        img, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)

    bin_img = cv2.resize(bin_img, (28, 28), interpolation=cv2.INTER_AREA)

    cv2.imwrite(dst_path, bin_img)
    print(f"saved: {fname}")

print("\nAll done.")
