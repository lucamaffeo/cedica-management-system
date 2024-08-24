## Calculadora con un case y funciones, input de signos y operandos
from src import *

def main():
    print("Calculadora")
    print("Ingrese el primer número")
    num1 = float(input())
    print("Ingrese el segundo número")
    num2 = float(input())
    print("Ingrese el signo de la operación")
    signo = input()
    match signo:
        case "+":
            pass
            #suma(num1, num2)
        case "-":
            pass
            #resta(num1, num2)
        case "*":
            pass
            #multiplicacion(num1, num2)
        case "/":
            pass
            #division(num1, num2)
        case _:
            print("Operación no válida")
