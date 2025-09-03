s_name=input('Enter the name of the student:')
s_no=int(input('Enter the number of the student:'))
s1,s2,s3=map(int,input('Enter three subjects marks:').split())
total=s1+s2+s3
print('The total marks of the student is:',total)
avg=(s1+s2+s3/3)
print('The average marks of the student is:',round(avg,2))