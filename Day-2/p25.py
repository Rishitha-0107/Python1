def fib(n):
    a,b=0,1
    cnt=0
    while cnt<n:
        print(a,end='')
        a,b=b,a+b
        cnt+=1
fib(5)