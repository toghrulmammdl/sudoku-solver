import cv2
import os

# =============================
# 1. Image oxu
# =============================
img = cv2.imread("download.png")
if img is None:
    raise FileNotFoundError("download.png tapılmadı")

h, w, _ = img.shape

# =============================
# 2. 3x3 ölçülər
# =============================
sub_h = h // 3
sub_w = w // 3

# =============================
# 3. Qovluq
# =============================
os.makedirs("subgrid", exist_ok=True)

# =============================
# 4. 3x3 böl və yaz
# =============================
for i in range(3):
    for j in range(3):
        y1 = i * sub_h
        y2 = (i + 1) * sub_h
        x1 = j * sub_w
        x2 = (j + 1) * sub_w

        sub = img[y1:y2, x1:x2]

        filename = f"subgrid/subgrid_{i}_{j}.png"
        cv2.imwrite(filename, sub)

        print(f"Yazıldı: {filename}")
