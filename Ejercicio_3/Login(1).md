# Login

## Explicación del programa

Primero se inicializan las variables con la cuenta y contraseña y la variable intentos

Se abre un while para limitar los intentos a 3

Primero se pregunta a terminal, cual es el usuario, después se checa si en su composición no esta vacio o con algún espacio, de ser detectado se manda mensaje a terminal sobre el error y se suma un intento, de no ser así continua con la contraseña, se pregunta la contraseña y se checa si cuenta con mínimo una letra y un numero, si no se regresa al inicio y suma un intento, si no, también se checa si el largo de la contraseña, si no es mínimo de 8 caracteres se detecta, se mandas mensaje a terminal del error y se vuelve a empezar con  un intento menos, por ultimo se checa si el usuario y contraseña son correctos; si si lo son se concede acceso, si no se pide que lo intente de nuevo y se le suma otro intento, pasados 3 intentos fallidos, se cierra el programa.

---

## Código en Python

```python
import sys

# Datos correctos
USER_DB = "admin"
PASS_DB = "Admin2026"

intentos = 0

while intentos < 3:
    print(f"\n--- INTENTO {intentos + 1} DE 3 ---")
    
    # --- BLOQUE DE USUARIO ---
    user = input("Usuario: ")
    
    # Verificación inmediata del usuario
    if chr(32) in user or user == "":
        print("Error: El usuario no puede tener espacios ni estar vacío.")
        intentos += 1
        if intentos == 3: break # Si falla 3 veces aquí, rompe el ciclo
        continue # Si no, vuelve a pedir el intento desde el inicio

    # --- BLOQUE DE CONTRASEÑA ---
    password = input("Contraseña: ")
    
    # Verificación inmediata de la contraseña (ASCII)
    tiene_letra = False
    tiene_num = False
    for c in password:
        if (ord(c) >= 65 and ord(c) <= 122): tiene_letra = True
        if (ord(c) >= 48 and ord(c) <= 57): tiene_num = True

    if len(password) < 8 or not tiene_letra or not tiene_num:
        print("Error: La contraseña debe tener 8+ caracteres, letras y números.")
        intentos += 1
        continue

    # --- VERIFICACIÓN FINAL ---
    if user == USER_DB and password == PASS_DB:
        print("\n¡Acceso concedido! Bienvenido.")
        break
    else:
        print("Credenciales incorrectas.")
        intentos += 1

# Cierre por seguridad
if intentos == 3:
    print("\nHas agotado tus intentos. El sistema se cerrará.")
    sys.exit()

# Menú Principal
print("Cargando Menú del Kiosco...")
```
