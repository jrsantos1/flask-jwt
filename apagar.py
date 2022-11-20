def soma(num1: int, num2: int):
    return num1 + num2

print(soma(2,3))

def soma_com_args(*args):
    lista = args
    print(type(lista))
    return sum(lista)

print(soma_com_args(3,5,7,9,8,7))
