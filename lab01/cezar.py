#Autor: Michał Wątroba 
#Indeks: 295965
import sys, math

def ceasar_encrypt(text, key):
    encrypted = ""
    for char in text:
        if 'a' <= char <= 'z':
            encrypted += chr((ord(char) + key - 97) % 26 + 97)
        elif 'A' <= char <= 'Z':
            encrypted += chr((ord(char) + key - 65) % 26 + 65)
        else:
            encrypted += char
    return encrypted

def ceasar_decrypt(text, key):
    return ceasar_encrypt(text, -key)

def ceasar_cryptoanalysis_with_text(text, known_text):
    for key in range(1, 26):
        decrypted = ceasar_decrypt(text, key)
        if decrypted.startswith(known_text):
            return key, decrypted
    return None, None

def ceasar_cryptoanalysis(text):
    results = []
    for key in range(1, 26):
        results.append(ceasar_decrypt(text, key))
    return results
  
def affine_encrypt(text, key):
    a, b = key
    if math.gcd(a, 26) != 1:
        raise ValueError("The condition GCD(a,26)=1 must be satisfied")
    encrypted = ""
    for char in text:
        if 'a' <= char <= 'z':
            encrypted += chr(((a * (ord(char) - 97) + b) % 26) + 97)
        elif 'A' <= char <= 'Z':
            encrypted += chr(((a * (ord(char) - 65) + b) % 26) + 65)
        else:
            encrypted += char
    return encrypted

def affine_decrypt(text, key):
    a, b = key
    a_inv = 0
    for i in range(1, 26):
        if (a * i) % 26 == 1:
            a_inv = i
    if a_inv == 0:
        raise ValueError("Modular inverse does not exist")
    decrypted = ""
    for char in text:
        if 'a' <= char <= 'z':
            decrypted += chr(((a_inv * ((ord(char) - 97) - b)) % 26) + 97)
        elif 'A' <= char <= 'Z':
            decrypted += chr(((a_inv * ((ord(char) - 65) - b)) % 26) + 65)
        else:
            decrypted += char
    return decrypted

def affine_cryptoanalysis_with_text(text, known_text):
    for a in range(1, 26):
        if math.gcd(a, 26) == 1:
            for b in range(0, 26):
                if a == 1 and b == 0:
                    continue
                try:
                    decrypted = affine_decrypt(text, (a, b))
                    if decrypted.startswith(known_text):
                        return (a, b), decrypted
                except ValueError:
                    continue
    return None, None

def affine_cryptoanalysis(text):
    results = []
    for a in range(1, 26):
        if math.gcd(a, 26) == 1:
            for b in range(0, 26):
                if a == 1 and b == 0:
                    continue
                try:
                    results.append(affine_decrypt(text, (a, b)))
                except ValueError:
                    continue
    return results

def main():
    if len(sys.argv) < 3:
        print("Uzycie: python cezar.py [-c|-a] [-e|-d|-j|-k]")
        return

    cypher_type = sys.argv[1]
    operation = sys.argv[2]

    if cypher_type == "-c":
        if operation == "-e":
            with open("plain.txt", "r") as file:
                text = file.read()
            with open("key.txt", "r") as file:
                try:
                    key = int(file.read().split()[0])
                except ValueError:
                    print("Invalid key")
                    return
            
            encrypted_text = ceasar_encrypt(text, key)
            with open("crypto.txt", "w") as file:
                file.write(encrypted_text)

        elif operation == "-d":
            with open("crypto.txt", "r") as file:
                text = file.read()
            with open("key.txt", "r") as file:
                try:
                    key = int(file.read().split()[0])
                except ValueError:
                    print("Invalid key")
                    return
                
            decrypted = ceasar_decrypt(text, key)
            with open("decrypt.txt", "w") as file:
                file.write(decrypted)

        elif operation == "-j":
            with open("crypto.txt", "r") as file:
                text = file.read()
            with open("extra.txt", "r") as file:
                known_text = file.read()

            key, decrypted = ceasar_cryptoanalysis_with_text(text, known_text)
            if key is not None:
                with open("key-found.txt", "w") as file:
                    file.write(f"{key}")
                with open("decrypt.txt", "w") as file:
                    file.write(decrypted)
            else:
                print("Key not found")
                
        elif operation == "-k":
            with open("crypto.txt", "r") as file:
                text = file.read()

            results = ceasar_cryptoanalysis(text)
            with open("decrypt.txt", "w") as file:
                for result in results:
                    file.write(result + "\n")
        else:
            print("Invalid operation")

    elif cypher_type == "-a":
        if operation == "-e":
            with open("plain.txt", "r") as file:
                text = file.read()
            with open("key.txt", "r") as file:
                key_parts = file.read().split()
                try:
                    b, a = int(key_parts[0]), int(key_parts[1])
                    key = (a, b)
                except (ValueError, IndexError):
                    print("Invalid key")
                    return
                
            try:
                encrypted = affine_encrypt(text, key)
                with open ("crypto.txt", "w") as file:
                    file.write(encrypted)
            except ValueError as e:
                print(e)
  
        elif operation == "-d":
            with open("crypto.txt", "r") as file:
                text = file.read()
            with open("key.txt", "r") as file:
                key_parts = file.read().split()
                try:
                    b, a = int(key_parts[0]), int(key_parts[1])
                    key = (a, b)
                except (ValueError, IndexError):
                    print("Invalid key")
                    return
                
            try:
                decrypted = affine_decrypt(text, key)
                with open("decrypt.txt", "w") as file:
                    file.write(decrypted)
            except ValueError as e:
                print(e) 

        elif operation == "-j":
            with open("crypto.txt", "r") as file:
                text = file.read()
            with open("extra.txt", "r") as file:
                known_text = file.read()
            
            key, decrypted = affine_cryptoanalysis_with_text(text, known_text)
            if key is not None:
                with open("key-found.txt", "w") as file:
                    file.write(f"{key[1]} {key[0]}")
                with open("decrypt.txt", "w") as file:
                    file.write(decrypted)
            else:
                print("Key not found")

        elif operation == "-k":
            with open("crypto.txt", "r") as file:
                text = file.read()
            results = affine_cryptoanalysis(text)
            with open("decrypt.txt", "w") as file:
                for result in results:
                    file.write(result + "\n")
        else:
            print("Invalid operation")
    else:
        print("Invalid cipher")

if __name__ == "__main__":
    main()