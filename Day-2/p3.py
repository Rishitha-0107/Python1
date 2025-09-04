def grade(a):
    if(a>=40):
        if(a>80):
            return "distinction"
        elif(71<=a<=80): 
            return "Grade A"
        elif(51<=a<=70):
            return "Grade B"
        else:
            return "Grade C"
    else:
        return "FAil"
print(grade(int(input('enter student marks'))))
