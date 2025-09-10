def numberofdup(l):
    dup = 0
    for i in range(len(l)):
        if l[i] in l[:i]:   
            dup += 1
    print("Number of duplicate elements:", dup)
l = [1, 1, 2, 2, 3, 4, 5]
numberofdup(l)
