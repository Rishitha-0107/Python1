def fun(var):
    if('a'<=var<='z') or ('A'<=var<='Z'):
        print('It is an alphabet')
    elif('0'<=var<='9'):
        print('It is a digit')
    else:
        print("it is a special character")
print(fun('*'))