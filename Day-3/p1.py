def create_list(n):
    l= [0] * n 
    for i in range(n):
        val=input(f"Enter element {i+1}:")
        l[i]=val
    return l
size=int(input("Enter number of elements:"))
result=create_list(size)
print("Final list:",result)
