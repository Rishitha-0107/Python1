c_no=int(input('Enter consumer number:'))
c_name=input('Enter consumer name:')
pmr=float(input('Enter present month reading:'))
lmr=float(input('Enter last month reading:'))
tu=pmr-lmr
print('total Units:',tu)
cbill=tu*3.80
print('Current bill:',cbill)
print(f"Consumer number is {c_no} and name is {c_name} and the total units are {tu} and Current bill is {cbill}")