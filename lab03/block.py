#Michał Wątroba
#indeks: 295965

import numpy as np
import hashlib
from PIL import Image

def hash_block(key: str, block_bytes: bytes) -> bytes:
    return hashlib.sha512((key + block_bytes.hex()).encode()).digest()

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def pad_image_to_block_size(img_array, block_size=8):
    height, width = img_array.shape
    new_height = ((height + block_size - 1) // block_size) * block_size
    new_width = ((width + block_size - 1) // block_size) * block_size
    padded = np.zeros((new_height, new_width), dtype=np.uint8)
    padded[:height, :width] = img_array
    return padded

def process_image_ecb_cbc(image_path: str, key_path: str = "key.txt"):
    try:
        img = Image.open(image_path).convert("L") 
    except FileNotFoundError:
        print(f"Nie znaleziono pliku obrazu: {image_path}")
        return
    
    try: 
        with open(key_path, "r") as f:
            key = f.read().strip()
    except FileNotFoundError:
        key = ''

    img_array = np.array(img)
    img_array = pad_image_to_block_size(img_array, 8)
    height, width = img_array.shape

    ecb_img_array = np.zeros_like(img_array)
    cbc_img_array = np.zeros_like(img_array)

    iv = hashlib.sha512((key + "_iv").encode()).digest()
    prev_cbc_hash = iv

    for y in range(0, height, 8):
        for x in range(0, width, 8):
            block = img_array[y:y+8, x:x+8]
            block_bytes = block.tobytes()

            # --- ECB ---
            block_hash_ecb = hash_block(key, block_bytes)

            # --- CBC ---
            xored = xor_bytes(block_bytes, prev_cbc_hash)
            block_hash_cbc = hash_block(key, xored)
            prev_cbc_hash = block_hash_cbc

            ecb_img_array[y:y+8, x:x+8] = np.frombuffer(block_hash_ecb, dtype=np.uint8).reshape((8, 8))
            cbc_img_array[y:y+8, x:x+8] = np.frombuffer(block_hash_cbc, dtype=np.uint8).reshape((8, 8))

    Image.fromarray(ecb_img_array).save("ecb_crypto.bmp")
    Image.fromarray(cbc_img_array).save("cbc_crypto.bmp")
    print("Zakończono generowanie obrazów: ecb_crypto.bmp oraz cbc_crypto.bmp")

if __name__ == "__main__":
    process_image_ecb_cbc("plain.bmp", "key.txt")