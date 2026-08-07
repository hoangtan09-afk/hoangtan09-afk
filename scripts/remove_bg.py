from pathlib import Path
from PIL import Image
from rembg import remove

# Thu muc goc cua project
BASE_DIR = Path(__file__).resolve().parent.parent

input_path = BASE_DIR / "assets" / "avatar.jpg"
output_path = BASE_DIR / "assets" / "avatar-nobg.png"

# Mo anh
image = Image.open(input_path).convert("RGBA")

# Xoa background
output = remove(image)

# Luu anh PNG trong suot
output.save(output_path)

print(f"Done: {output_path}")



