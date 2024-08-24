def division(num1, num2):
    try:
        result = num1 / num2
        return result
    except ZeroDivisionError:
        return "Error: No se puede dividir entre cero."
    except TypeError:
        return "Error: Ambos parámetros deben ser números."
