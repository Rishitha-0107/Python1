#program to give frequency of elements in a list
def freq(l):
    for i in range(len(l)):
        if l[i] in l[:i]:
            continue 
        count=0
        for j in l:
            if j==l[i]:
                count+=1
        print(l[i],"appears",count,"times")
l = [1, 2, 2, 3, 1, 4, 2, 3]
freq(l)
