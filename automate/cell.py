import cv2
import os

INPUT_DIR = "subgrid_clean"
OUTPUT_DIR = "cells_raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

INNER_CROP = 0.08
for fname in os.listdir(INPUT_DIR):
    if not fname.endswith(".png"):
        continue

    path = os.path.join(INPUT_DIR, fname)
    img = cv2.imread(path)

    if img is None:
        continue

    h, w, _ = img.shape

    cell_h = h // 3
    cell_w = w // 3

    base = os.path.splitext(fname)[0]

    for i in range(3):
        for j in range(3):
            y1 = i * cell_h
            y2 = (i + 1) * cell_h
            x1 = j * cell_w
            x2 = (j + 1) * cell_w

            cell = img[y1:y2, x1:x2]

            ch, cw, _ = cell.shape
            dy = int(ch * INNER_CROP)
            dx = int(cw * INNER_CROP)

            cell = cell[dy:ch-dy, dx:cw-dx]
            cell_gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)


            out_name = f"{base}_cell_{i}_{j}.png"
            out_path = os.path.join(OUTPUT_DIR, out_name)

            cv2.imwrite(out_path, cell_gray)
            print(f"Saved: {out_name}")
