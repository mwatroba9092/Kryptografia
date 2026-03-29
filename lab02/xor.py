# Michał Wątroba
# indeks: 295965 

import os, argparse, base64

def prepare_file():
    if not os.path.exists("orig.txt"):
        print("Błąd: Plik orig.txt nie został znaleziony.")
        return
    
    with open("orig.txt", "r", encoding="utf-8") as file:
        text = file.read()

    line_length = 64
    text = ' '.join(text.splitlines())
    
    filtered_text = ''.join(char for char in text if char.isalpha() or char.isspace()).lower()

    lines = []
    for i in range(0, len(filtered_text), line_length):
        if i + line_length <= len(filtered_text):
            lines.append(filtered_text[i:i + line_length])
        else:
            last_line = filtered_text[i:]
            padded_line = last_line + ' ' * (line_length - len(last_line))
            lines.append(padded_line)

    try:
        with open("plain.txt", "w", encoding="utf-8") as file:
            file.write('\n'.join(lines))
        print("Sukces: Przygotowano plik plain.txt.")
    except Exception as e:
        print(f"Błąd podczas zapisu do plain.txt: {e}")

def encrypt_file():
    if not os.path.exists("plain.txt"):
        print("Błąd: Plik plain.txt nie został znaleziony.")
        return
    if not os.path.exists("key.txt"):
        print("Błąd: Plik key.txt nie został znaleziony.")
        return

    with open("plain.txt", "r", encoding="utf-8") as file:
        plaintext = file.read()
    with open("key.txt", "r", encoding="utf-8") as file:
        key = file.read()

    encrypted_lines = []
    for line in plaintext.splitlines():
        if len(line) > 64:
            print("Błąd: Linia przekracza 64 znaki. Sprawdź plik wejściowy.")
            return
        
        encrypted_bytes = bytearray()
        for i in range(len(line)):
            key_temp = key[i % len(key)]
            encrypted_bytes.append(ord(line[i]) ^ ord(key_temp))
        
        encrypted_lines.append(encrypted_bytes)

    try:
        with open("crypto.txt", "w", encoding="utf-8") as file:  
            for enc_bytes in encrypted_lines:
                b64_encoded = base64.b64encode(enc_bytes).decode('ascii')
                file.write(b64_encoded + '\n')
        print("Sukces: Zaszyfrowano tekst. Wynik w crypto.txt.")
    except Exception as e:
        print(f"Błąd podczas zapisu do crypto.txt: {e}")

def cryptoanalysis():
    if not os.path.exists("crypto.txt"):
        print("Błąd: Plik crypto.txt nie został znaleziony.")
        return

    with open("crypto.txt", "r", encoding="utf-8") as file:
        encrypted_lines = file.readlines()
        
    key_length = 64 
    possible_key = bytearray([0] * key_length)
    key_found = [False] * key_length 
    
    decoded_lines = [base64.b64decode(line.strip()) for line in encrypted_lines]

    for pos in range(key_length):
        bytes_at_pos = [line[pos] for line in decoded_lines if pos < len(line)]
        
        best_key = 0
        best_score = -1

        for byte_i in bytes_at_pos:
            cand_key = byte_i ^ 32
            
            score = 0
            is_valid = True

            for byte_j in bytes_at_pos:
                dec = byte_j ^ cand_key
                if dec == 32:
                    score += 3
                elif 97 <= dec <= 122 or 65 <= dec <= 90:
                    score += 2
                else:
                    is_valid = False
                    break
            
            if is_valid and score > best_score:
                best_score = score
                best_key = cand_key
                key_found[pos] = True

        if key_found[pos]:
            possible_key[pos] = best_key

    decrypted_lines = []
    for line in decoded_lines:
        decrypted = []
        for i, byte in enumerate(line):
            if i < key_length and key_found[i]:
                dec_char = byte ^ possible_key[i]
                if 97 <= dec_char <= 122 or 65 <= dec_char <= 90 or dec_char == 32: 
                    decrypted.append(chr(dec_char))
                else:
                    decrypted.append('_')
            else:
                decrypted.append('_')
            
        decrypted_lines.append(''.join(decrypted))
        
    try:
        with open("decrypt.txt", "w", encoding="utf-8") as file:
            file.write('\n'.join(decrypted_lines))
        print("Sukces: Kryptoanaliza zakończona. Sprawdź plik decrypt.txt.")
    except Exception as e:
        print(f"Błąd podczas zapisu do decrypt.txt: {e}")

def main():
    parser = argparse.ArgumentParser(description="Program do szyfrowania XOR i kryptoanalizy.")
    parser.add_argument("-p", "--prepare", action="store_true")
    parser.add_argument("-e", "--encrypt", action="store_true")
    parser.add_argument("-k", "--cryptoanalysis", action="store_true")
    args = parser.parse_args()

    if args.prepare:
        prepare_file()
    elif args.encrypt:
        encrypt_file()
    elif args.cryptoanalysis:
        cryptoanalysis()
    else:
        print("Użyj flagi: -p (--prepare), -e (--encrypt) lub -k (--cryptoanalysis).")

if __name__ == "__main__":
    main()