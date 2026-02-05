# 🐍 Guía rápida: Python + Entorno virtual + NumPy (Windows)

> Documentación de respaldo para futuras prácticas  
> Autor: Dean Yeshua Guerrero Rivera

---

## 1️⃣ Verificar que Python correcto esté activo

En la terminal de VS Code ejecuta:

```bash
where python
```

Debe apuntar a algo como:

```text
...\Proyecto\env\Scripts\python.exe
```

Si ves rutas como `msys64` ❌, no estás usando el Python correcto.

---

## 2️⃣ Crear el entorno virtual

Dentro de la carpeta del proyecto:

```bash
python -m venv env
```

---

## 3️⃣ Activar el entorno virtual

### En PowerShell:

```bash
env\Scripts\Activate.ps1
```

Cuando está activo, la terminal se ve así:

![Entorno virtual activo](/Ejercicio_1/assets/El_env.png)

Si no aparece `(env)` al inicio, **el entorno NO está activo**.

---

## 4️⃣ Seleccionar el intérprete correcto en VS Code

1. Presiona `Ctrl + Shift + P`
2. Escribe: `Python: Select Interpreter`
3. Elige el que diga algo como:

```text
Python 3.12.x ('env')
```

Así debe verse:

![Seleccionar intérprete](/Ejercicio_1/assets/Interprete.png)

---

## 5️⃣ Instalar NumPy (dentro del entorno)

Con el entorno activo:

```bash
python -m pip install numpy
```

Verifica instalación:

```bash
pip show numpy
```

---

## 6️⃣ Probar NumPy en un archivo

Crea un archivo llamado `main.py`:

```python
import numpy as np

x = np.random.randint(1, 11)
print(x)
```

Ejecuta:

```bash
python main.py
```

---

## 7️⃣ Confirmar que NumPy funciona correctamente

En VS Code, al escribir:

```python
np.
```

Debe aparecer el **autocompletado** de NumPy, así:

![Autocompletado NumPy](/Ejercicio_1/assets/numpy.png)

Si aparece:
- `random`
- `array`
- `mean`
- `zeros`

✅ NumPy está bien instalado y funcionando.

---

## 🧠 Notas importantes

- Siempre activa el entorno antes de trabajar
- Nunca instales librerías sin el entorno activo
- Un entorno = un proyecto

---

## ✅ Checklist rápido

- [x] Python correcto
- [x] Entorno activo `(env)`
- [x] Intérprete seleccionado
- [x] NumPy instalado
- [x] Autocompletado funcionando

---

📌 *Este archivo sirve como guía de respaldo para futuras prácticas.*
