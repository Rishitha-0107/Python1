def oddeven(l):
    o=0
    e=0
    for i in l:
        if i%2==0:
           e+=1
        else:
            o+=1
    return e,o
l=[5,7,8,12,14,53,66,78]
even,odds=oddeven(l)
print('Even numbers:',even)
print("odd numbers:",odds)