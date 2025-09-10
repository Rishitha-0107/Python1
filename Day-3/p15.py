#program to search all occurences of a character in given string
def char_occurrences(s, ch):
    p=[] 
    for i in range(len(s)):
        if s[i]==ch:
            p.append(i)
    if p:
        print(f"Character '{ch}' found at positions:", p)
    else:
        print(f"Character '{ch}' not found in the string.")
char_occurrences(input("Enter a string: "),input("Enter character to search: "))
