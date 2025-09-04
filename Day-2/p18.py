def prime_numbers(n):
    for num in range(2,n+1):   # loop through numbers from 2 to n
        is_prime=True
        for i in range(2,num):
            if num%i==0:
                is_prime=False
                break
        if is_prime:
            print(num, end=" ")
n=int(input("Enter n: "))
prime_numbers(n)