# Login

## Explicación del programa

Primero se inicializan las variables con la cuenta y contraseña y la variable intentos

Se abre un while para limitar los intentos a 3

Primero se pregunta a terminal, cual es el usuario, después se checa si en su composición no esta vacio o con algún espacio, de ser detectado se manda mensaje a terminal sobre el error y se suma un intento, de no ser así continua con la contraseña, se pregunta la contraseña y se checa si cuenta con mínimo una letra y un numero, si no se regresa al inicio y suma un intento, si no, también se checa si el largo de la contraseña, si no es mínimo de 8 caracteres se detecta, se mandas mensaje a terminal del error y se vuelve a empezar con  un intento menos, por ultimo se checa si el usuario y contraseña son correctos; si si lo son se concede acceso, si no se pide que lo intente de nuevo y se le suma otro intento, pasados 3 intentos fallidos, se cierra el programa.

---

## Código en Python

```python
import sys


Usuario = "admin"
Contraseña = "Admin2026"
intento = 0

while intento < 3:

   print(f"\n INTENTO {intento + 1} DE 3 ")
   user = input("Usuario :  ")

   if user == "":
      print(" No pusiste nada w ")
      intento += 1
      if intento == 3: break
      continue

   if chr(32) in user:
      print(" No quiero espacio jeje")
      intento += 1
      if intento == 3: break
      continue

   passw = input("Contraseña:  ")

   letra = False
   numero = False

   for c in passw:
      if (ord(c) >= 65 and ord(c) <= 122): letra=True
      if (ord(c) >= 48 and ord(c) <= 57): numero=True

   if len(passw) < 8 : 
      print("Imposible procesar, nimodo (ta corta )")
      intento += 1
      continue
   if not letra:
      print(" Te falta poner letras w")
      intento += 1
      continue
   if not numero:
      print(" Te falta poner numeros w")
      intento += 1
      continue

   if user == Usuario and passw == Contraseña:
      print("ACCESO CONCEDIDO FELIcIDAdES JAJAJAJAJAJJQAJAJAJAJAJAJAJAJAJAJAJAJAJA ")
      print("Bienvenido a Loquendo City") 
      break
   else:
      print("no")
      intento += 1

      

   

   if intento == 3:
      print ("Ya no hijo, no te creo (te pasaste de intentos)")
      sys.exit()

```
![Entorno virtual activo](/Ejercicio_3/assets/soo.jpg)
