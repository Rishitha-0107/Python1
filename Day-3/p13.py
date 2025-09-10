#write a program to count total number of vowels and cnsonants in a string
def cntstr(s):
    v=0
    c=0
    s=s.lower()
    for ch in s:
        if ch.isalpha():
            if ch in 'aeiou':
                v+=1
            else:
                c+=1
    print("Vowles:",v)
    print("Consonants:",c)
cntstr(input("enter a string: "))