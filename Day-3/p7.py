def uniq(l):
    for i in range(len(l)):
        if l[i] not in l[:i]:  
            print(l[i], end=" ")
l = [1, 2, 2, 3, 1, 4, 2, 3]
uniq(l)

        
