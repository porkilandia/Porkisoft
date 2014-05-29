'''Aplicacion que permite ingresar 2 numeros y dependiendo de la
 operacion que elijamos muestra el resultado, se requiere completar lo siguiente:

 * la operacion resta
 * la operacion Multiplicacion
 * la operacion Division
  * Validar que el numero que se esta ingresando sea positivo.

  * Numero mayor Numero menor(este punto adicional lo realizara el alumno :BRYAN ZAMBRANO)
  '''

import os# libreria para poder limpiar la pantalla cada vez que inicia el programa

def capturaNum1():#Metodo que captura el el primer numero del usuario
    num1 = int(raw_input("Digite el primer numero: "))
    return num1

def capturaNum2():#Metodo que captura el segundo numero del usuario
    num2 = int(raw_input("Digite el segundo numero: "))
    return num2

def suma(num1,num2):
    resultado = num1 + num2
    os.system('clear')#si trabajan en windows cambiar el contenido de los parentesis por 'cls'
                      #os.system('clear') limpia la pantalla
    print("*******************************************")
    print("El Resultado de la suma es: %d"%resultado)#imprime el resultado de la operacion
    print("*******************************************")

def resta(num1,num2):
    os.system('clear')


def multiplicacion(num1,num2):
    os.system('clear')


def division(num1,num2):
    os.system('clear')


def numeroMayor(num1,num2):
    os.system('clear')


def menu(opcion,num1,num2):

    if opcion == 1:
        suma(num1,num2)
    if opcion == 2:
        resta(num1,num2)
    if opcion == 3:
        multiplicacion(num1,num2)
    if opcion == 4:
        division(num1,num2)



opcion = 0
num1 = 0
num2 = 0
os.system('clear')

while opcion != 6:#Mientras que la opcion que digite el usuario sea diferente de 6 el programa seguira funcionando

    if num1 and num2 :# si num1 y num2 son diferentes de 0 captura la opcion
        print("---------------------------------------------")
        print("************ MENU DE APLICACIONES************")
        print("---------------------------------------------")
        print("1. Suma")
        print("2. Resta")
        print("3. Multiplicacion")
        print("4. Division")
        print("5. Numero mayor")
        print("6. Salir")
        print("*******************************************")
        opcion = int(raw_input("digite su opcion: "))
        print("*******************************************")
    else:# de lo contrario pedira los datos de los numeros para poder realizar las operaciones
        num1 = capturaNum1()
        num2 = capturaNum2()

    menu(opcion,num1,num2)#Llamamos al metodo menu para evaluar el requerimiento del usuario
