def is_armstrong(n):
    temp=n
    digits=len(str(n))   # count number of digits
    total=0
    while n>0:
        digit=n%10
        total+=digit ** digits
        n//=10
    return temp==total
num = int(input("Enter a number: "))
if is_armstrong(num):
    print(num, "is an Armstrong number")
else:
    print(num, "is not an Armstrong number")
