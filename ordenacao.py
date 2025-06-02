

def ordenacao_bubble_sort(vetor):
    """
    Ordenacão Bubble Sort.
    
    Args:
        vetor (list): Lista de números a ser ordenada
    
    Returns:
        list: Lista ordenada em ordem crescente
    """
    v = vetor.copy()
    n = len(v)
    
    for rodada in range(n - 1):
        for i in range(n - 1 - rodada):
            if v[i] > v[i + 1]:
                v[i], v[i + 1] = v[i + 1], v[i]
    
    return v


if __name__ == "__main__":

    vetor_exemplo = [5, 3, 2, 4, 7, 1, 0, 6]
    
    print("=" * 50)
    print("DEMONSTRAÇÃO DO BUBBLE SORT")
    print("=" * 50)
    
    resultado = ordenacao_bubble_sort(vetor_exemplo)

    print(vetor_exemplo)
    print("Resultado:")
    print(resultado)
    