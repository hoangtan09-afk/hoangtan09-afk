

from pathlib import Path
import cv2

BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "assets" / "avatar-nobg.png"
output_path = BASE_DIR / "assets" / "avatar-prepped.png"

# Đọc ảnh, giữ cả kênh alpha (background trong suốt)
image = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)

if image is None:
    raise FileNotFoundError(f"Cannot open: {input_path}")

# Tách RGB và alpha
bgr = image[:, :, :3]
alpha = image[:, :, 3]

# Chuyển grayscale
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

# Tăng contrast cục bộ
clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

enhanced = clahe.apply(gray)

# Ghép grayscale thành 3 channel + giữ background trong suốt
result = cv2.merge([
    enhanced,
    enhanced,
    enhanced,
    alpha
])

cv2.imwrite(str(output_path), result)

print(f"Done: {output_path}")