def greatest(a,b,c):
    if(a>b):
        if(a>c):
            print('a is greatest among all numbers')
        else:
            print('c is greatest')
    else:
        if(b>c):
            print('b is greatest')
        else:
            print('c is greatest')
print(greatest(3,54,5))