# storng - sum of factorials of digits is same as number
def factorial(n):
    if(n==0 or n==1):
        return 1
    else:
        return n*factorial(n-1)
def strong(n):
    sum=0
    m=n
    while(n!=0):
        r=n%10
        sum=sum+factorial(r)
        n=n//10
    return (sum==m)
s=strong(int(input("Enter n : ")))
print("Strong")if (s==True) else print("Not Strong")