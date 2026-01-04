import os
import cv2

CELL_DIR = "cells"         
TEMPLATE_DIR = "templates" 
IMG_SIZE = 28

EMPTY_RATIO_THRESHOLD = 0.01
SIMILARITY_THRESHOLD = 0.75   

templates = {}

for d in range(1, 10):
    path = os.path.join(TEMPLATE_DIR, f"{d}.png")
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Template not found: {path}")

    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    templates[d] = img

def is_empty(cell_bin):
    ratio = cv2.countNonZero(cell_bin) / (IMG_SIZE * IMG_SIZE)
    return ratio < EMPTY_RATIO_THRESHOLD


def similarity(a, b):
    diff = cv2.bitwise_xor(a, b)
    return 1.0 - (cv2.countNonZero(diff) / (IMG_SIZE * IMG_SIZE))


def match_template(cell_bin):
    best_digit = 0
    best_score = 0.0

    for digit, tmpl in templates.items():
        score = similarity(cell_bin, tmpl)
        if score > best_score:
            best_score = score
            best_digit = digit

    if best_score < SIMILARITY_THRESHOLD:
        return 0

    return best_digit


grid = [[0 for _ in range(9)] for _ in range(9)]

for fname in os.listdir(CELL_DIR):
    if not fname.endswith(".png"):
        continue

    parts = fname.replace(".png", "").split("_")
    sg_r, sg_c, c_r, c_c = map(int, [parts[1], parts[2], parts[4], parts[5]])

    row = sg_r * 3 + c_r
    col = sg_c * 3 + c_c

    cell = cv2.imread(os.path.join(CELL_DIR, fname), cv2.IMREAD_GRAYSCALE)
    if cell is None:
        continue

    cell = cv2.resize(cell, (IMG_SIZE, IMG_SIZE))

    if is_empty(cell):
        grid[row][col] = 0
    else:
        grid[row][col] = match_template(cell)


for r in grid:
    print(r)
