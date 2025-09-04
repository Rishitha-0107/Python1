def is_palindrome(num):
    temp=num
    rev=0
    while num>0:
        digit=num % 10
        rev=rev*10+digit
        num//=10
    return temp==rev
def palindrome_numbers(n):
    for i in range(1,n+1):
        if is_palindrome(i):
            print(i, end=" ")
n=int(input("Enter n: "))
palindrome_numbers(n)