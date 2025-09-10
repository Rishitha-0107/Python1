#write a program to count total number of words in atring
def wordcnt(s):
    w=s.split()   
    print("Total number of words:", len(w))
wordcnt(input("Enter a string: "))
