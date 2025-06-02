def soma_multiplos_3_ou_5(x):
    """
    Calcula a soma de todos os números que são múltiplos de 3 ou 5
    abaixo do número X fornecido como parâmetro.
    
    Args:
        x (int): O limite superior (não incluído na soma)
    
    Returns:
        int: A soma de todos os múltiplos de 3 ou 5 abaixo de X
    """
    soma = 0

    for numero in range(1, x):
        if numero % 3 == 0 or numero % 5 == 0:
            soma += numero
    
    return soma


if __name__ == "__main__":
    exemplos = [10, 20, 50, 100]

    for exemplo in exemplos:
        resultado = soma_multiplos_3_ou_5(exemplo)
        print(f"Soma dos múltiplos de 3 ou 5 abaixo de {exemplo}: {resultado}")
        print("\n")
    
    