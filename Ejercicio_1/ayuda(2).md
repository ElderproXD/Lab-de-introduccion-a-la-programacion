# 🐍 Guía paso a paso: Python + Entorno Virtual + NumPy en Windows

> Archivo de apoyo personal para futuras instalaciones  
> Compatible con **GitHub Markdown (.md)**  
> Todos los comandos están en bloques copiables

---

## 1️⃣ Verificar que Python esté instalado correctamente

Abrir **PowerShell o CMD**  
❌ NO usar MSYS

```bash
py --version
```

Debe mostrar algo como:

```text
Python 3.12.x
```

Esto confirma que se está usando el Python oficial de Windows.

---

## 2️⃣ Crear la carpeta del proyecto

Ejemplo:

```text
mi_proyecto_python/
```

Abrir esta carpeta con **Visual Studio Code**.

---

## 3️⃣ Crear el entorno virtual

Desde la terminal de VS Code:

```bash
py -3.12 -m venv env
```

Esto crea un entorno virtual llamado `env`.

---

## 4️⃣ Activar el entorno virtual

```bash
env\Scripts\activate
```

Si todo está bien, la terminal mostrará:

```text
(env)
```

### 📸 Así debe verse la terminal

![Entorno virtual activo](/Ejercicio_1/assets/El_env.png)

---

## 5️⃣ Seleccionar el intérprete correcto en VS Code

1. Presionar `Ctrl + Shift + P`
2. Buscar:

```text
Python: Select Interpreter
```

3. Elegir:

```text
Python 3.12 (env)
```

### 📸 Dónde elegir el intérprete

![Seleccionar intérprete en VS Code](/Ejercicio_1/assets/Interprete.png)

Esto asegura que VS Code use el Python del entorno.

---

## 6️⃣ Actualizar pip (PASO CLAVE)

Con el entorno activado:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Esto evita errores al instalar librerías como NumPy.

---

## 7️⃣ Instalar NumPy correctamente (sin errores)

```bash
pip install numpy --only-binary=:all:
```

✔️ Evita compilación  
✔️ No usa MSYS  
✔️ Compatible con Windows

---

## 8️⃣ Verificar que NumPy está instalado

### Opción A – pip

```bash
pip show numpy
```

### Opción B – Python

```bash
python -c "import numpy as np; print(np.__version__)"
```

Si imprime la versión → NumPy funciona ✅

---

## 9️⃣ Crear archivo de prueba

Crear un archivo llamado `main.py`

```python
import numpy as np


def main() -> None:
    arreglo = np.array([1, 2, 3])
    print(arreglo)
    print(np.__version__)


if __name__ == "__main__":
    main()
```

Ejecutar:

```bash
python main.py
```

---

## 🔍 Cómo saber que todo está bien

- La terminal muestra `(env)`
- `import numpy` no da errores
- `np.array()` funciona
- Al escribir `np.` aparece autocompletado en VS Code

### 📸 Autocompletado correcto de NumPy

![Autocompletado NumPy](/Ejercicio_1/assets/numpy.png)

---

## ⚠️ Notas importantes

- ❌ NO usar Python de:
```text
C:\msys64\...
```

- ✅ Usar siempre:
```bash
py
```

- Cada proyecto debe tener su propio entorno virtual
- Las librerías se instalan **dentro del env**, no global

---

## 🧠 Resumen rápido (copiar y pegar)

```bash
py -3.12 -m venv env
env\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install numpy --only-binary=:all:
```

---

📌 **Fin del archivo de ayuda**
