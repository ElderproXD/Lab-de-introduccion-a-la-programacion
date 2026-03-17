# --- CONSTANTES ---
VERDE = '\033[92m'
ROJO = '\033[91m'
RESET = '\033[0m'
USUARIO_ADMIN = "admin"
PASSWORD_ADMIN = "Admin2026"

def clasificar_numero():
    print("\n --- Clasificar número ---")
    try:
        num = int(input("\n Ingresa un número: "))
    except ValueError:
        print(f"{ROJO}Eso no es un número w.{RESET}")
        return

    if num == 0:
        print("Es 0 pibe, no es ni par ni impar")
    elif num % 2 == 0:
        print(f"{num} es par")
    else:
        print("Es impar")   

    if num < 0:
        print(f"{num} Es un número negativo w")
    elif num > 0:
        print(f"{num} Es un número positivo")

def categoria_edad():
    print("\n --- Categoría de edad y sus permisos ---")
    try:
        edad = int(input("Escribe tu edad plosillo: "))
    except ValueError:
        print(f"{ROJO}Edad inválida.{RESET}")
        return False
        
    ine = input("¿Trais INE? (S/N): ").upper()
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
     
    # Retornamos el estado del Modo God para usarlo si se necesita
    modo_god = False
    if edad >= 21 and ine == "S":
        print(f"{VERDE}Modo God activado.{RESET}")
        modo_god = True
    else: 
        print("Permisos faltantes para el Modo God.")
        
    return modo_god

def calcular_tarifa():
    print("\n --- Calcular tarifa de Pase Diario ---")
    precio_base = 200.0
    recargo = 0.0
    porcentaje_descuento = 0
    
    # Validamos que ponga una edad real
    while True:
        try:
            edad_t = int(input("Edad (0 a 120): "))
            if 0 <= edad_t <= 120:
                break 
            else:
                print(f"{ROJO}No mientas cabron muchacho.{RESET}")
        except ValueError:
            print(f"{ROJO}Mete un número we.{RESET}")

    if 0 <= edad_t <= 12:
        porcentaje_descuento += 50
    elif 13 <= edad_t <= 17:
        porcentaje_descuento += 20
    elif edad_t >= 65:
        porcentaje_descuento += 30
    else:
        print(f"{ROJO}No tiene descuento por edad{RESET}")   
             
    try:
        dia = int(input("Día de la semana (1=Lun ... 7=Dom): "))
    except ValueError:
        dia = 1
        
    if dia in (6, 7): 
        recargo = precio_base * 0.10
        print(f"{ROJO}Recargo por FIN DE SEMANA{RESET}")
        
    estudiante = input("¿Es estudiambre? (S/N): ").upper()
    if estudiante == "S":
        print(f"{VERDE}Estudiante confirmado (-15%){RESET}")
        if edad_t >= 13:
            porcentaje_descuento += 15
            print(f"{VERDE}Descuento por estudiante aplicado{RESET}")
    else:
        print(f"{ROJO}No es estudiante{RESET}")

    miembro = input("¿Tienes el Modo God? (S/N): ").upper()
    if miembro == "S":
        print(f"{VERDE}Modo God Confirmado (-10%){RESET}")
        porcentaje_descuento += 10
    else:
        print(f"{ROJO}NO ES GOD{RESET}")

    pago = input("Método de pago: B (Billetazo) o T (Tarjetazo): ").upper()
    if pago == "B":
        porcentaje_descuento += 5 
        print(f"{VERDE}DESCUENTO POR PAGO EN EFECTIVO DEL 5%{RESET}")
        
    # --- AQUÍ ESTÁ EL BUG ARREGLADO (El límite va ANTES de la resta) ---
    if porcentaje_descuento > 60:
        porcentaje_descuento = 60
        print(f"{ROJO}Límite de descuento 60% alcanzado{RESET}")

    descuento_dinero = precio_base * (porcentaje_descuento / 100) 
    total_final = precio_base + recargo - descuento_dinero
    
    print("\n--- RECIBO DE COMPRA ---")
    print(f"Precio base:         ${precio_base:.2f}")
    if recargo > 0:
        print(f"{ROJO}Recargo DE FINDE: +${recargo:.2f}{RESET}")
    print(f"Descuento aplicado:   {porcentaje_descuento}% (-${descuento_dinero:.2f})")
    print("-" * 25)
    print(f"{VERDE}TOTAL A PAGAR:       ${total_final:.2f}{RESET}")

def login():
    intento = 0
    
    while intento < 3:
        print(f"\n --- INTENTO {intento + 1} DE 3 --- ")
        user = input("Usuario: ")

        if not user:
            print(f"{ROJO}No pusiste nada w{RESET}")
            intento += 1
            continue

        if " " in user: 
            print(f"{ROJO}No quiero espacio jeje{RESET}")
            intento += 1
            continue

        passw = input("Contraseña: ")

        letra = any(c.isalpha() for c in passw)
        numero = any(c.isdigit() for c in passw)

        if len(passw) < 8: 
            print(f"{ROJO}Imposible procesar, nimodo (ta corta){RESET}")
            intento += 1
            continue
        if not letra:
            print(f"{ROJO}Te falta poner letras w{RESET}")
            intento += 1
            continue
        if not numero:
            print(f"{ROJO}Te falta poner números w{RESET}")
            intento += 1
            continue

        if user == USUARIO_ADMIN and passw == PASSWORD_ADMIN:
            print(f"\n{VERDE}ACCESO CONCEDIDO FELICIDADES JAJAJAJAJAJA{RESET}")
            print("Bienvenido a Loquendo City")
            
            while True:
                print("\n--- MENÚ PRINCIPAL ---")
                print("1. Clasificar numero")
                print("2. Categoria de edad y sus permisos")
                print("3. Calcular tarifa de Pase Diario")
                print("4. Cerrando sesion")
                print("5. Adios")
                
                menu = input("\nElige pibe: ")
                
                # Usando el match en lugar de ifs
                match menu:
                    case "1":
                        clasificar_numero()
                    case "2":
                        categoria_edad()
                    case "3":
                        calcular_tarifa()
                    case "4":
                        print("\nCerrando sesión... regresando al login w")
                        break # Rompe el ciclo del menú, reinicia intentos
                    case "5":
                        print("\nAdiós!")
                        return # Termina la función main y apaga el programa
                    case _:
                        print(f"{ROJO}Opción no válida, intenta de nuevo plosillo.{RESET}")
            
            intento = 0 
            continue 
            
        else:
            print(f"{ROJO}no{RESET}")
            intento += 1

    if intento >= 3:
        print(f"{ROJO}Ya no hijo, no te creo (te pasaste de intentos){RESET}")

# Este es el estándar de Python para ejecutar la función principal
if __name__ == "__main__":
    login()
