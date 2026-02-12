numero = int(input("Ingresa un número entero: "))

# ---------- BINARIO ----------
n = numero
binario = ""

while n > 0:
    residuo = n % 2
    binario = str(residuo) + binario
    n = n // 2

print("Binario:", binario)


# ---------- OCTAL ----------
n = numero
octal = ""

while n > 0:
    residuo = n % 8
    octal = str(residuo) + octal
    n = n // 8

print("Octal:", octal)


# ---------- HEXADECIMAL ----------
n = numero
hexadecimal = ""

while n > 0:
    residuo = n % 16

    if residuo == 10:
        hexadecimal = "A" + hexadecimal
    elif residuo == 11:
        hexadecimal = "B" + hexadecimal
    elif residuo == 12:
        hexadecimal = "C" + hexadecimal
    elif residuo == 13:
        hexadecimal = "D" + hexadecimal
    elif residuo == 14:
        hexadecimal = "E" + hexadecimal
    elif residuo == 15:
        hexadecimal = "F" + hexadecimal
    else:
        hexadecimal = str(residuo) + hexadecimal

    n = n // 16

print("Hexadecimal:", hexadecimal)
