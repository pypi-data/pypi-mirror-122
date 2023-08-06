def primosEratostenes(n):
    """
    Aplicamos el algoritmo conocido como la criba de Eratostenes
    para calcular los numeros primos entre 1 y n
    """
    posibles_primos = [i for i in range(2, n + 1)]
    for j in range(2,n + 1):
        sig_num = 2*j
        while sig_num <= n:
            if sig_num in posibles_primos:
                posibles_primos.remove(sig_num)
            sig_num += j
    for primo in posibles_primos:
        print(f'{primo} es primo')