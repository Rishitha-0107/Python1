def check_string(s):
    alph=0
    digi= 0
    special=0
    for ch in s:
        if ch.isalpha():
            alph+=1
        elif ch.isdigit():
            digi+=1
        else:
            special += 1
    print("Alphabets:", alph)
    print("Digits:", digi)
    print("Special Characters:", special)
s=input("Enter a string: ")
check_string(s)

