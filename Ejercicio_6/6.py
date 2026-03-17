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
            print("\n Clasificar numero")
            num = int(input("\n Ingresa un numero: "))
         
            if num == 0:
               print("")
            elif num < 0:
               print(str(num)," Es un numero negativo w")
            elif num > 0:
               print(str(num)," Es un numero positivo")  

            if num == 0:
               print("Es 0 pibe, no es ni par ni impar")
            elif num % 2 == 0 and num != 0:
               print(str(num)," es par")
            else:
               print("Es impar")   
                 
         elif menu == "2":
            print("\n Categoria de edad y sus permisos")
            edad = int(input("Escribe tu edad plosillo: "))
            INE = input("¿Trais INE? (S/N): ").upper()
            lic = input("¿Trais Licencia? (S/N): ").upper()
             
           
            if edad < 0 or edad > 120:
                print("Edad inválida.")
            elif 0 <= edad <= 12:
               print("Estás en la niñez.")
            elif 13 <= edad <= 17:
               print("Estás en la adolescencia.")
            elif 18 <= edad <= 64:
               print("Estás en la adultez.")
            else:
               print("Eres un adulto mayor.")
             
           
            if edad >= 18:
               print("Puedes comprar sin tutor y registrarte.")
            elif edad >= 13:
               print("Puedes registrarte, pero ocupas tutor para comprar.")
            else: 
               print("Requieres un tutor para registrarte.") 
             
            
            if edad >= 18 and lic == "S":
               print("Puedes conducir.")
            else:
               print("No puedes conducir.")
             
           
            if edad >= 21 and INE == "S":
               print("Modo God activado.")
              
            else: 
               print("No permisos faltantes para el Modo God.")
            
         elif menu == "3":
            print("\n  Calcular tarifa de Pase Diario ")
            precio_base = 200
            recargo = 0
            porcentaje_descuento = 0
            while True:
               edad_t = int(input("Edad (0 a 120): "))
               if 0 <= edad_t <= 120:
                  break 
               else:
                  print(f"\n {ROJO}No mientas cabron muchacho.{RESET}")


            if 0 <= edad_t <= 12:
               porcentaje_descuento += 50
            elif 13 <= edad_t <= 17:
               porcentaje_descuento += 20
            elif edad_t >= 65:
               porcentaje_descuento += 30
            else:
               print(f"{ROJO}No Tiene descuento por edad {RESET} ")        
            dia = int(input("Día de la semana (1=Lun ... 7=Dom): "))
            if dia == 6 or dia == 7: 
               recargo = precio_base * 0.10
               print(f"\n {ROJO} Recargo por FIN DE SEMANA {RESET}")
            estudiante = input("¿Es estudiambre? (S/N): ").upper()
            if estudiante == "S":
               estudiante = True
               print(f"\n {VERDE}Estudiante confirmado (-15%) {RESET}")
               
            else:
               print(f"\n {ROJO}No es estudiante {RESET}")
               estudiante = False  

            if estudiante == True and edad_t >= 13:
               porcentaje_descuento += 15
               print(f"{VERDE} Descuento por estudiante (-15%) {RESET}")

            miembro = input("¿Tienes el Modo God? (S/N): ").upper()
            if miembro == "S":
               print(f"\n {VERDE}Modo God Confirmado(-10%){RESET}")
               miembro = True
            else:
               print(f"\n {ROJO} NO ES GOD {RESET}")
               miembro = False

            if miembro == True:
               porcentaje_descuento += 10

            pago = input("Metodo de pago: B (Billetazo) o T (Tarjetazo): ").upper()
            if pago == "B":
               porcentaje_descuento += 5 
               print(f"{VERDE} DESCUENTO POR PAGO EN EFECTIVO DEL 5% {RESET}")
               
           

            descuento_dinero = precio_base * (porcentaje_descuento / 100) 
            total_final = precio_base + recargo - descuento_dinero
            print("\n--- RECIBO DE COMPRA ---")
            print(f"Precio base:  ${precio_base}")
            if recargo > 0:
               print(f"{ROJO}Recargo DE FINDE: +${recargo}{RESET}")
            if porcentaje_descuento > 60:
               porcentaje_descuento = 60
               print(f" {ROJO} Limite de descuento 60% {RESET}")
            print(f"Descuento aplicado:   {porcentaje_descuento}% (-${descuento_dinero})")
            print(f"------------------------")
            print(f"{VERDE}TOTAL A PAGAR:       ${total_final}{RESET}")

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
