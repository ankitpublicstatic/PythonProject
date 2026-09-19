# pip install pillow
from PIL import Image
import io
import os

target_bytes = 60 * 1024  # 61,440 bytes      
input_path = "ankit_signature.jpeg"
output_path = "ankit_signature_60kb.jpg"

img = Image.open(input_path).convert("RGB")

# Step 1: Save at high quality into a byte buffer
buffer = io.BytesIO()
img.save(buffer, format="JPEG", quality=95)
data = buffer.getvalue()

# Step 2: Pad with trailing null bytes to hit exactly 60 KB
if len(data) < target_bytes:
    data += b'\x00' * (target_bytes - len(data))
else:
    # If starting size is larger, reduce quality first
    for q in range(90, 10, -5):
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=q)
        data = buffer.getvalue()
        if len(data) <= target_bytes:
            data += b'\x00' * (target_bytes - len(data))
            break

with open(output_path, "wb") as f:
    f.write(data)

print(f"File saved: {os.path.getsize(output_path)} bytes")