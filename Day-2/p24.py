def prime_factors_unique(n):
    factors = []
    for i in range(2, n + 1):
        if n % i == 0:
            is_prime = True
            for j in range(2, i):
                if i % j == 0:
                    is_prime = False
                    break
            if is_prime:
                factors.append(i)
    return factors
print(prime_factors_unique(8)) 
print(prime_factors_unique(18))
