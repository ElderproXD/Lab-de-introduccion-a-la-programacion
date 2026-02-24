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

     










 
