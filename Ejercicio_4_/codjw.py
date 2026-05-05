Usuario = "admin"
Contraseña = "Admin2026"
intento = 0
VERDE = '\033[92m'
ROJO = '\033[91m'
RESET = '\033[0m'

seguir_en_programa = True 

while seguir_en_programa and intento < 3:
   print(f"\n --- INTENTO {intento + 1} DE 3 --- ")
   user = input("Usuario :  ")

   if user == "":
      print(" No pusiste nada w ")
      intento += 1
      continue

   if chr(32) in user: 
      print(" No quiero espacio jeje")
      intento += 1
      continue

   passw = input("Contraseña:  ")

   letra = any(c.isalpha() for c in passw)
   numero = any(c.isdigit() for c in passw)

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
      print(f"\n{VERDE}ACCESO CONCEDIDO FELIcIDAdES JAJAJAJAJAJJQAJAJAJAJAJAJAJAJAJAJAJAJAJA{RESET}")
      print("Bienvenido a Loquendo City")
      
      while True:
         print("\n--- MENÚ PRINCIPAL ---")
         print("1. Clasificar numero")
         print("2. Categoria de edad y sus permisos")
         print("3. Calcular tarifa")
         print("4. Cerrando sesion")
         print("5. Adios")
         
         menu = input("\nElije pibe: ")
         
         if menu == "1":
            print("\n[🛠️ Opción 1 desactivada - No hace nada por ahora ]")
            # Aquí iba la lógica de clasificar números
                 
         elif menu == "2":
            print("\n[🛠️ Opción 2 desactivada - No hace nada por ahora ]")
            # Aquí iba la lógica de categorías de edad
            
         elif menu == "3":
            print("\n[🛠️ Opción 3 desactivada - No hace nada por ahora ]")
            # Aquí iba la lógica de calcular tarifa
            
         elif menu == "4":
            print("\nCerrando sesion... regresando al login w")
            break 
            
         elif menu == "5":
            print("\nAdios!")
            seguir_en_programa = False 
            break 
            
         else:
            print("\nOpción no válida, intenta de nuevo.")
      
      intento = 0 
      continue 
      
   else:
      print("no")
      intento += 1

if intento >= 3:
   print ("Ya no hijo, no te creo (te pasaste de intentos)")
