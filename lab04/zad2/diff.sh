#!/bin/bash

# Michał Wątroba 
# nr. indeksu: 295965

if [ ! -f "hash-.pdf" ]; then
    echo "Błąd: Brak pliku hash-.pdf w bieżącym katalogu!"
    exit 1
fi

if [ ! -f "personal.txt" ]; then
    echo "Błąd: Brak pliku personal.txt w bieżącym katalogu!"
    exit 1
fi

echo "Tworzenie pliku personal_.txt"
cp personal.txt personal_.txt
echo "" >> personal_.txt

echo "Obliczanie haszy i porównywanie bitów"

> diff.txt

FUNKCJE=("md5sum" "sha1sum" "sha224sum" "sha256sum" "sha384sum" "sha512sum" "b2sum")

for f in "${FUNKCJE[@]}"; do
    cmd1="cat hash-.pdf personal.txt | $f"
    cmd2="cat hash-.pdf personal_.txt | $f"

    echo "$cmd1" >> diff.txt
    echo "$cmd2" >> diff.txt

    hash1=$(eval $cmd1 | awk '{print $1}')
    hash2=$(eval $cmd2 | awk '{print $1}')

    echo "$hash1" >> diff.txt
    echo "$hash2" >> diff.txt

    python3 -c "
h1 = int('$hash1', 16)
h2 = int('$hash2', 16)
xor_val = h1 ^ h2
diff_bits = bin(xor_val).count('1')
total_bits = len('$hash1') * 4
percent = round((diff_bits / total_bits) * 100)
print(f'Liczba różniących się bitów: {diff_bits} z {total_bits}, procentowo: {percent}%.')
" >> diff.txt

    echo "" >> diff.txt
done

echo "Gotowe, Wygenerowano plik diff.txt."