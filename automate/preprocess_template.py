import cv2
import os

SRC = "templates_raw"
DST = "templates"
os.makedirs(DST, exist_ok=True)

for d in range(1, 10):
    img = cv2.imread(f"{SRC}/{d}.png", cv2.IMREAD_GRAYSCALE)

    _, bin = cv2.threshold(img, 0, 255,
                            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    bin = cv2.resize(bin, (28, 28))
    cv2.imwrite(f"{DST}/{d}.png", bin)

