def addset(n):
    s = []  
    for i in range(n):
        val = int(input("Enter a value: "))
        if val not in s:
            s += [val]
        else:
            print(val, "is already in the set, skipping.")
    print("Set elements:", s)
n = int(input("How many elements do you want to add? "))
addset(n)

