
def fatorial_recursivo(n):
    if n == 0:
        return 1
    else:
        return n * fatorial_recursivo(n-1)
    


if __name__ == "__main__":
    numero = 5
    
    fatorial = fatorial_recursivo(numero)

    print(f"O fatorial de {numero} é {fatorial}")