def strlen(n,n1):
    cnt=0
    c=0
    for i in n:
        cnt+=1
    print(cnt)
    for i in n1:
        c+=1
    print(c)
    if(n==n1):
        print("both strinngs are same")
    else:
        print("Both strings are not same")
    print("Concatenation of two strings:",n+n1)
strlen("Rishi","rishi")