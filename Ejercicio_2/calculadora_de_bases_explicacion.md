# 📘 Calculadora de Bases Numéricas

Conversión manual de un número **decimal** a **binario, octal y hexadecimal**, utilizando el método matemático de **divisiones sucesivas**, sin funciones especiales de Python.

---

## 🧠 Descripción general

El programa pide un número a pantalla, después lo iguala a la variable `n` y se empieza a calcular cada conversión.

El procedimiento es el mismo para todas las bases:

- Se obtiene el **residuo** con el operador `%`.
- El residuo se guarda como dígito de la nueva base.
- El número se divide usando `//` para continuar el proceso.
- El ciclo se repite mientras `n > 0`.

---

## 🧑‍💻 Código del programa

```python
numero = int(input("Ingresa un número entero: "))

# BINARIO
n = numero
binario = ""

while n > 0:
    residuo = n % 2
    binario = str(residuo) + binario
    n = n // 2

print("Binario:", binario)


# OCTAL
n = numero
octal = ""

while n > 0:
    residuo = n % 8
    octal = str(residuo) + octal
    n = n // 8

print("Octal:", octal)


# HEXADECIMAL
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
```

---

## 🔢 Explicación del proceso

### 🔹 Binario

Entra el número decimal, se le saca el residuo de 2 con `%` y se guarda en la variable `residuo`. Este residuo se convierte a cadena y se guarda en la variable `binario`, procurando meterlos de forma en que el primer residuo sea el último dígito del número binario.

Esto se repite por cada vuelta del ciclo `while` mientras que `n > 0`. El valor de `n` se actualiza usando `n = n // 2`, donde `//` elimina la parte decimal para evitar errores.

Al finalizar el ciclo, se muestra a pantalla el resultado del número binario.

---

### 🔹 Octal

Se sigue exactamente el mismo procedimiento que para el binario, solo que en este caso se usa `residuo = n % 8` y `n = n // 8`, ya que se busca representar el número decimal en base 8.

El resultado se guarda y se muestra en la variable `octal`.

---

### 🔹 Hexadecimal

El proceso es similar a los anteriores, pero con algunos detalles extras. Los valores del 10 al 15 no se representan como números, sino como letras:

- **A = 10**
- **B = 11**
- **C = 12**
- **D = 13**
- **E = 14**
- **F = 15**

Primero se obtiene el residuo con `residuo = n % 16`. Posteriormente, este residuo se compara y, si corresponde a alguno de los valores anteriores, se sustituye por la letra adecuada. Si no, se deja tal cual, ya que los valores del 0 al 9 no cambian.

El dígito obtenido se guarda en la variable `hexadecimal`, manteniendo el mismo orden que en las otras bases, dejando el primer residuo como el último dígito. Finalmente, se muestra el resultado en pantalla.

---
![Entorno virtual activo](/Ejercicio_2/assets/sis.jpg)

