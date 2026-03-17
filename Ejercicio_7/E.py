def e1():
      print("Ejercicio 1 repetir palabra")
      x = str( input("Escriba alguna palabra: "))
      for i in range(10):
            print(x)


def e2(): 
      print("Ejercicio 2 Años cumplidos")     
      x = int( input("¿Cual es tu edad? "))
      for i in range(x):
            print("Feliz cumpleaños",x)

def e3():
      print("Ejercicio 3 numeros impares hazta donde tu quieras")
      x = int( input("Escriba un numero: "))
      for i in range(x):
            if i % 2 != 0:
                  print(i)

def e4():
      print("Ejercicio 4 cuenta hacia atras")
      x = int( input("Escriba un numero: "))
      for i in range(x, 0, -1):
            print(i ,",")

def e5():
      print("caluladora de inversion, interes anual, numeros de años y capital obtenido")
      inversion = float( input("¿Cuanto dinero desea invertir? "))
      interes = float( input("¿Cual es el interes anual? "))
      años = int(input("¿Cuantos años desea invertir? "))
      for i in range(años):
            inversion = inversion + (inversion * (interes / 100))
      print(f"El capital obtenido después de {años} años es: {inversion:.2f}")

def e6():
      print("Ejercicio 6 triangulo de asteriscos")
      x = int( input("Escriba un numero: "))
      for i in range(1, x + 1):
            print("*" * i)

def e7():
      print("Ejercicio 7 tabla de multiplicar del 1 al 10")
      for i in range(1, 11):
               print(f"Tabla del {i}:")
               for j in range(1, 11):
                     print(f"{i} x {j} = {i * j}")
               print()           

def e8():
     print("Ejercicio 8: Triángulo de números impares")

     n = int(input("Escriba un número entero: "))

     for x in range(1, n + 1):
    
          max_impar = 2 * x - 1
    
          for num in range(max_impar, 0, -2):
           print(num, end=" ")
           print()  


def e9():
      print("Ejercicio 9: La contraseña")
      print("Escribe una contraseña")
      contraseña= str(input("Contraseña:  "))

      
      while True:
            print("¿Cuál es la contraseña?")
            confirmacion = str(input("Contraseña:  "))
            input
            if contraseña == confirmacion:
                  print("Contraseña correcta")
                  break
            else:
                  print("Contraseña incorrecta")

      
def e10():
      print("Ejercicio 10: Primo o no primo")
      numero = int(input("Escribe un número entero: "))
      if numero < 2:
            print(f"{numero} no es primo.")
      else:
            es_primo = True
            for i in range(2, int(numero**0.5) + 1):
                  if numero % i == 0:
                        es_primo = False
                        break
            if es_primo:
                  print(f"{numero} es primo.")
            else:
                  print(f"{numero} no es primo.")


def e11():
      print("Ejercicio 11: descomponiendo la palabra")
      palabra = str(input("Escribe una palabra: "))
      for letra in palabra:
            print(letra)

   
def e12():
      print("Ejercicio 12: ¿Cuantas veces aparece la letra en la frase?")
      frase = str(input("Escribe una frase: "))
      letra = str(input("Escribe una letra: "))
      contador = 0
      for X in frase:
            if X == letra:
                  contador += 1
      print(f"La letra '{letra}' aparece {contador} veces en la frase.")
     

def e13():
      print("Ejercicio 13: Eco hasta escribir 'salir'")
      while True:
         texto = str(input("Escribe algo (o 'salir' para terminar): "))
         if texto == "salir":
            print("Adio plosillo")
            break
         else:
            print(texto)



      while True:
            print("\n" + "="*40)
            print("MENU DE EJERCICIOS")
            print("="*40)
            print("1. Ejercicio 1 - Repetir palabra")
            print("2. Ejercicio 2 - Años cumplidos")
            print("3. Ejercicio 3 - Números impares")
            print("4. Ejercicio 4 - Cuenta hacia atrás")
            print("5. Ejercicio 5 - Calculadora de inversión")
            print("6. Ejercicio 6 - Triángulo de asteriscos")
            print("7. Ejercicio 7 - Tabla de multiplicar")
            print("8. Ejercicio 8 - Triángulo de números impares")
            print("9. Ejercicio 9 - La contraseña")
            print("10. Ejercicio 10 - Primo o no primo")
            print("11. Ejercicio 11 - Descomponiendo la palabra")
            print("12. Ejercicio 12 - Contar letra en frase")
            print("13. Ejercicio 13 - Eco hasta salir")
            print("0. Salir del programa")
            print("="*40)
            
            opcion = input("Selecciona un ejercicio: ")
            
            match opcion:
               case "1":
                  e1()
               case "2":
                  e2()
               case "3":
                  e3()
               case "4":
                  e4()
               case "5":
                  e5()
               case "6":
                  e6()
               case "7":
                  e7()
               case "8":
                  e8()
               case "9":
                  e9()
               case "10":
                  e10()
               case "11":
                  e11()
               case "12":
                  e12()
               case "13":
                  e13()
               case "0":
                  print("adios ☺"*70)
                  break
               case _:
                  print("Opción no válida. Intenta de nuevo.")
            
            input("\nPresiona Enter para volver al menú...")


