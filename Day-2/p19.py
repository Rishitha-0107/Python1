def is_palindrome(n):
    temp=n
    rev= 0
    while n>0:
        digit=n%10
        rev=rev*10+digit
        n//=10
    return temp==rev
num = int(input("Enter a number: "))
if is_palindrome(num):
    print(num, "is a palindrome")
else:
    print(num, "is not a palindrome")
