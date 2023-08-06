def primeNumber(n):
    primos = []
    for i in range(2,n+1):
        prime = True
        for j in range(2, i):
            if (i%j) == 0:
                prime = False
        if prime:
            primos.append(i)
    return(primos)

#print(primeNumber(100))


