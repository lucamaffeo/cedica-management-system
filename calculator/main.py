## Calculadora con un case y funciones, input de signos y operandos
from src.resta import resta
from src.suma import suma
from src.division import division
from src.multiplicacion import multiplicacion

def main():
    result = None
    print("Calculadora")
    print("Ingrese el primer número")
    num1 = float(input())
    print("Ingrese el segundo número")
    num2 = float(input())
    print("Ingrese el signo de la operación")
    signo = input()
    try:
        match signo:
            case "+":
                pass
                result = suma(num1, num2)
            case "-":
                pass
                result = resta(num1, num2)
            case "*":
                pass
                result = multiplicacion(num1, num2)
            case "/":
                pass
                result = division(num1, num2)
            case _:
                raise ValueError("Operación no válida")
    except ValueError as e:
        print(e)
    else:
        print("El resultado es", result)
    
if __name__ == "__main__":
    main()  
