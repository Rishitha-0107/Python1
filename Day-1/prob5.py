p,r,t=map(int,input('Enter principle amount,rate of intesrst and total number of months'.split(' ')))
si=(p*r*t)/100
print('Simple Interest is:',si)
ta=p+si
print('Total amount:',ta)