# Function to calculate sum of digits
def sum_of_digits(num):
    total=0
    while num>0:
        digit= num % 10   # extract last digit
        total+=digit     # add to sum
        num//=10         # remove last digit
    return total
number=int(input("Enter a number: "))
print("Sum of digits:", sum_of_digits(number))


