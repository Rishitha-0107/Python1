def fact(n):
    fact=0
    for i in range(1,n+1):
        if(n%i==0):
            fact+=fact
            print(i)
        else:
            i+=1
fact(8)