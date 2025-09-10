def studrec():
    t1=(6732,"rishi",98)
    t2=(6766,"sun",93)
    t3=(6777,"moon",88)
    t4=(6792,"ishi",90)
    t5=(6742,"ira",96)
    students=[t1,t2,t3,t4,t5]
    print("Student Records (Roll No, Name, Marks):")
    for s in students:
        print(s)
    high=students[0]
    for s in students:
        if s[2]>high[2]:   
            high=s
    print("\nStudent with highest marks:", high[1],"(",high[2],")")
    print("\nStudents who scored more than 75 marks:")
    for s in students:
        if s[2]>75:
            print(s[1],"-",s[2])
studrec()