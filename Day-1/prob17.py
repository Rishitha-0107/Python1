#given year is leap year or not
def year(x):
    if(x%4==0 and x%100!=0) or (x%400==0):
        print('given year is leap year')
    else:
        print('given year is not a leap year')
print(year(2016))