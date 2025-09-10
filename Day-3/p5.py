#program to delete element at specified positon
def delele(l, pos):
    n=len(l)
    for i in range(pos, n-1):
        l[i]=l[i+1]
    l=l[:n-1]
    return l
l=[10,20,30,40,50]
pos=int(input("Enter position to delete: "))
print("List after deletion:", delele(l, pos))
