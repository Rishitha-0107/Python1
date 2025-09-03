#given character is alphabet or not
def alph(char):
    if('a'<=char<='z') or ('A'<=char<='Z'):
        print('the given character is alphabet')
    else:
        print('the given character is not an alphabet')

print(alph('c'))
